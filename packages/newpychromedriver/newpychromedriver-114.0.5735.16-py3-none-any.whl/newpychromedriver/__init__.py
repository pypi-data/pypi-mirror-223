#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
Copyright: Copyright 2019, unipark.io
'''
import os
import platform
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 系统 驱动目录配置
CONFIGS = [
    # linux
    { "system": re.compile(r"Linux", re.I), "arch": re.compile(r"(x(86_)?|amd)64$", re.I), "folder": "chromedriver-linux64", "filename": "chromedriver"}, 
    # mac
    { "system": re.compile(r"Darwin", re.I), "arch": re.compile(r"arm64$", re.I), "folder": "chromedriver-mac-arm64", "filename": "chromedriver"},
    { "system": re.compile(r"Darwin", re.I), "arch": re.compile(r"x86_64$", re.I), "folder": "chromedriver-mac-x64", "filename": "chromedriver"},
    # windows  
    { "system": re.compile(r"Windows", re.I), "arch": re.compile(r"x86$", re.I), "folder": "chromedriver-win32", "filename": "chromedriver.exe"},
    { "system": re.compile(r"Windows", re.I), "arch": re.compile(r"(x(86_)?|amd)64$", re.I), "folder": "chromedriver-win64", "filename": "chromedriver.exe"}, 
]


def get_system_arch(system, arch):
    system = system if system else platform.system()
    arch = arch if arch else platform.machine()

    for item in CONFIGS:
        if item['system'].match(system) and item['arch'].match(arch):
            return dict( filename = item['filename'], folder = item["folder"] )


def _get_filename():
    system = platform.system()
    arch = platform.machine()

    result = get_system_arch(system, arch)
    print('匹配结果',result)
    if result:
        path = os.path.join(BASE_DIR, result['folder'], result['filename'])

    if not os.path.exists(path):
        raise FileNotFoundError('ChromeDriver for {}({}) ' 'is not found.'.format(system, arch))
    
    return path



chromedriver_path = _get_filename()
