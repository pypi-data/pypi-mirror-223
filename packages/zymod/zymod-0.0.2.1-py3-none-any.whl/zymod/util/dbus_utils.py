#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import dbus


# /usr/bin/nginx -g 'pid /run/nginx.pid; error_log stderr;'
# ['/usr/bin/nginx', '-g', 'pid /run/nginx.pid; error_log stderr;']
def cmd_array_to_str(array):
    s = ""

    if len(array) == 1:
        s = array[0]
    else:
        for v in array:
            if ' ' in v:
                s += "'{}' ".format(v)
            else:
                s += "{} ".format(v)

    return s.strip()
