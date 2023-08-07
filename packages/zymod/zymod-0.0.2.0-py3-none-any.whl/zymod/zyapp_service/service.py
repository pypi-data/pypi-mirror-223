#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# zyapp_service获取指定应用运行状态（服务或进程状态），用于上层代码判断应用的运行情况
#
# 优先级：
#
# 1. 获取应用进程PID；
#
#     1.1 方法一：尝试使用dbus从Systemd查找应用对应的系统服务；
#
#         a. Systemd->从系统服务设置获取PIDFile；
#
#             1) 从指定的PID文件获取【应用进程PID】
#
#         b. Systemd->不满足条件a，则从系统服务设置ExecMainPID属性，获取【应用进程PID】；
#         c. Systemd->不满足条件b，则从系统服务设置MainPID属性，获取【应用进程PID】；
#
#     1.2 方法二：直接从指定的PID文件获获取【应用进程PID】；
# 3. 从/proc扫描进程PID的名称、进程状态、执行路径、命令行等。
#
# 通过不同优先级策略，使代码很好的支持使用Systemd（现代）或SysVinit（过时）的Linux发行版。
#
# 1. 基于Systemd的Linux发行版：通过dbus从Systemd获取系统服务设置
# 2. 非Systemd的Linux发行版：直接读取指定的PID文件获取相关数据

from happy_python import HappyLog
from happy_python import HappyPyException
from zymod.systemd import ZySystemdService
from zymod.systemd import ZySystemdUnit
from zymod.util import cmd_array_to_str
from zymod.zyprocfs import ProcItems, from_pid_file
from pathlib import Path

hlog = HappyLog.get_instance()


class ZyAppServiceType:
    SystemD = "SystemD"
    SysVinit = "SysVinit"

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value

    @staticmethod
    def from_string(origin):
        if origin == "systemd":
            return ZyAppServiceType.SystemD
        elif origin == "init":
            return ZyAppServiceType.SysVinit
        else:
            return ZyAppServiceType.other(origin)

    @staticmethod
    def other(value):
        return ZyAppServiceType(f"Other({value})")


class ZyAppServiceStatus:
    service_active: str
    service_main_pid: int
    service_exec_main_pid: int
    proc_id: int
    proc_name: str
    proc_state: str
    proc_exe: str
    proc_cmd: str

    def __init__(self):
        self.service_active = "n/a"
        self.service_main_pid = 0
        self.service_exec_main_pid = 0
        self.proc_id = 0
        self.proc_name = "n/a"
        self.proc_state = "n/a"
        self.proc_exe = "n/a"
        self.proc_cmd = "n/a"


class ZyAppService:
    init_sys: ZyAppServiceType
    service_name: str
    service_desc: str
    service_type: str
    service_pid_file: str
    service_exec_start: str
    service_exec_stop: str
    service_exec_reload: str
    app_pid_file: str
    status: ZyAppServiceStatus

    def __init__(self, service_name: str, pid_file: str):
        self.init_sys = ZyAppServiceType.other("none")
        self.service_name = service_name
        self.service_desc = "n/a"
        self.service_type = "n/a"
        self.service_pid_file = "n/a"
        self.service_exec_start = "n/a"
        self.service_exec_stop = "n/a"
        self.service_exec_reload = "n/a"
        self.app_pid_file = pid_file
        self.status = ZyAppServiceStatus()

    def setup(self):
        fn_name = "ZyAppService.setup"
        hlog.enter_func(fn_name)

        proc_items = ProcItems(1)
        pid = 0
        try:
            proc_items.scan()
        except HappyPyException as e:
            hlog.error(e)
            hlog.exit_func(fn_name)
            return False

        self.init_sys = ZyAppServiceType.from_string(proc_items.name)

        if self.init_sys == ZyAppServiceType.SystemD:

            zy_service_props = ZySystemdService(self.service_name).get_props()
            zy_unit_props = ZySystemdUnit(self.service_name).get_props()

            pid_file_result = zy_service_props.pid_file

            self.service_desc = zy_unit_props.desc
            self.service_type = zy_service_props.type
            self.service_pid_file = pid_file_result

            if self.app_pid_file is None:
                self.app_pid_file = self.service_pid_file

            pid_file = ""

            if Path(self.app_pid_file).exists():
                pid_file = self.app_pid_file
            elif Path(self.service_pid_file).exists():
                pid_file = self.service_pid_file

            if pid_file:
                try:
                    pid_result = from_pid_file(self.app_pid_file)
                    pid = pid_result
                except FileNotFoundError:
                    hlog.error("从指定PID文件（%s）获取PID失败" % self.app_pid_file)
                    return False

            self.status.service_main_pid = zy_service_props.main_pid
            self.status.service_exec_main_pid = zy_service_props.exec_main_pid

            if self.status.service_exec_main_pid != 0:
                pid = self.status.service_exec_main_pid
            elif self.status.service_main_pid != 0:
                pid = self.status.service_main_pid

            self.status.service_active = zy_unit_props.active_state

            start_v = zy_service_props.exec_start
            (_, start_cmdline, _, _, _, _, _, _, _, _) = start_v[0]
            self.service_exec_start = cmd_array_to_str(start_cmdline)

            stop_v = zy_service_props.exec_stop
            if stop_v:
                (_, stop_cmdline, _, _, _, _, _, _, _, _) = stop_v[0]
                self.service_exec_stop = cmd_array_to_str(stop_cmdline)

            reload_v = zy_service_props.exec_reload
            if reload_v:
                (_, reload_cmdline, _, _, _, _, _, _, _, _) = reload_v[0]
                self.service_exec_reload = cmd_array_to_str(reload_cmdline)

            if pid == 0:
                hlog.error("从系统服务和指定PID文件都无法获得进程PID")
                hlog.exit_func(fn_name)
                return False

            proc_items = ProcItems(pid)
            try:
                proc_items.scan()
            except HappyPyException as e:
                hlog.error(e)
                return False

            self.status.proc_id = proc_items.pid
            self.status.proc_state = proc_items.state
            self.status.proc_cmd = proc_items.cmdline
            self.status.proc_exe = proc_items.exe
            self.status.proc_name = proc_items.name

            return True

        elif self.init_sys == ZyAppServiceType.SysVinit:
            pid_file = ""

            if Path(self.app_pid_file).exists():
                pid_file = self.app_pid_file
            elif Path(self.service_pid_file).exists():
                pid_file = self.service_pid_file

            if pid_file:
                try:
                    pid_result = from_pid_file(self.app_pid_file)
                    pid = pid_result
                except FileNotFoundError:
                    hlog.error("从指定PID文件（%s）获取PID失败" % self.app_pid_file)

                if pid == 0:
                    hlog.error("从系统服务和指定PID文件都无法获得进程PID")
                    hlog.exit_func(fn_name)
                    return False

                proc_items = ProcItems(pid)
                proc_items.scan()

                self.status.proc_id = proc_items.pid
                self.status.proc_state = proc_items.state
                self.status.proc_cmd = proc_items.cmdline
                self.status.proc_exe = proc_items.exe
                self.status.proc_name = proc_items.name

                return True
        else:
            hlog.error("未知的初始化系统类型")
            hlog.exit_func(fn_name)
            return False
