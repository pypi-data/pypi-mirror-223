import datetime
import json
import os
import sys
import subprocess
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from .tools import data


pid = 0
processes = {}


class Process:
    def __init__(self, absfile, default_dir, handler, console=None):
        global pid
        self.absfile = absfile
        self.id = pid + 1
        pid += 1
        os.chdir(os.path.dirname(absfile))
        args = [sys.executable, absfile] if absfile.endswith('.py') else ([absfile] if not console else console.split())
        self.process = subprocess.Popen(args=args, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stdin=subprocess.PIPE)
        os.chdir(default_dir)
        self.handler = handler
        self.name = os.path.split(absfile)[1] if not console else 'console'
        self.alive = True
        processes[self.id] = self
        self.thread = Thread(target=self.daemon)
        self.thread.start()

    def daemon(self):
        try:
            mk = InlineKeyboardMarkup()
            mk.row(InlineKeyboardButton('communicate',
                                        callback_data=json.dumps({"handler": "communicate", "data": self.id})))
            mk.row(InlineKeyboardButton('❌', callback_data='{"handler": "close"}'))
            while self.getalive():
                self.get_out(mk)
            mk = InlineKeyboardMarkup()
            mk.row(InlineKeyboardButton('❌', callback_data='{"handler": "close"}'))
            err = self.process.stderr.read().decode()
            self.handler.send_message(chat_id=data['host'],
                                      text=f"process {self.name} was completed{' with error ' + err if err else ''}",
                                      reply_markup=mk)
            processes.pop(self.id)
        except Exception as e:
            print(e)
            self.kill()
            processes.pop(self.id)
            mk = InlineKeyboardMarkup()
            mk.row(InlineKeyboardButton('❌', callback_data='{"handler": "close"}'))
            self.handler.send_message(chat_id=data['host'],
                                      text=f"process {self.name} was completed with RePrIm error",
                                      reply_markup=mk)

    def communicate(self, info):
        self.process.stdin.write(str(info).encode())
        self.process.stdin.close()

    def get_out(self, mk):
        try:
            out = self.read_io(2)[:4096]
            if out:
                self.handler.send_message(chat_id=data['host'], text=f"out from {self.name}:\n{out}",
                                          reply_markup=mk)
        except subprocess.TimeoutExpired:
            pass

    def read_io(self, timeout):
        endtime = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        stdout = ''
        while endtime > datetime.datetime.now():
            out = self.process.stdout.readline().decode()
            if out:
                stdout += out
        return stdout

    def kill(self):
        try:
            if self.name.endswith('.py'):
                self.process.kill()
            else:
                subprocess.Popen(f'taskkill /im {self.name} /f')
        except:
            pass

    def getalive(self):
        return self.process.poll() is None
