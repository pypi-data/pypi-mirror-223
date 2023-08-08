#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import psutil
from zymod.util import cmd_array_to_str
from happy_python import HappyPyException


def from_pid_file(path: str):
    try:
        with open(path, 'r') as file:
            pid = int(file.read().strip())
            return pid
    except FileNotFoundError as e:
        return e


class ProcItems:
    def __init__(self, pid):
        self.pid = pid
        self.name = ""
        self.cmdline = ""
        self.exe = ""
        self.state = ""

    def scan(self):
        try:
            proc = psutil.Process(self.pid)
            proc_status = proc.status()

            self.name = proc.name()
            self.state = proc_status
            self.cmdline = cmd_array_to_str((proc.cmdline()))
            self.exe = proc.exe()
        except Exception:
            raise HappyPyException(err="获取进程（PID=%s）数据失败" % self.pid)
