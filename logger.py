# -*- coding:utf-8 -*-
import logging
import os
from datetime import date
import traceback

LOG_PATH = os.path.join('/var/log/project', 'Log')

class _(object):
    def __init__(self, title, message):
        self.title = title
        self.message = message

    def __str__(self):
        return '%s >>> %s' % (self.title, self.message)

class __(object):
    def __init__(self, title, message=''):
        self.title = title
        self.message = message

    def __str__(self):
        _str = '%s >>> %s' % (self.title, self.message)
        _str += '【错误信息】%s' % (traceback.format_exc())
        for _index, _v in enumerate(traceback.format_stack()):
            _str += '[%s] %s' % (_index, _v)

        return _str

class FilterByLevelName(logging.Filter):
    def __init__(self, name='', levelname = 'DEBUG'):
        super(FilterByLevelName, self).__init__(name=name)
        self.levelname = levelname

    def filter(self, record):
        if record.levelname != self.levelname:
            return False
        if self.nlen == 0:
            return True
        elif self.name == record.name:
            return True
        elif record.name == '__main__':
            return True
        elif record.name.find(self.name, 0, self.nlen) != 0:
            return False

        return True


def createFileHandleByLevel(levelname):
    filename = levelname.lower()+str(date.today())+'.log'
    filename = os.path.join(LOG_PATH, filename)
    file_handle = logging.FileHandler(filename=filename)
    file_handle.setFormatter(format_handle)
    _filter= FilterByLevelName(name='app', levelname=levelname)
    file_handle.addFilter(_filter)

    return file_handle

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

format_handle = logging.Formatter('%(asctime)s Process:%(process)d Thread:%(thread)d %(name)s %(pathname)s[line:%(lineno)d] %(levelname)s'+os.linesep+'%(message)s'+os.linesep)

handle = []
level = [
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR'
]

# 设置控制台输出
console_handle = logging.StreamHandler()
console_handle.setFormatter(format_handle)
_filter_name = logging.Filter(name='app')
console_handle.addFilter(_filter_name)
handle.append(console_handle)

for _level in level:
    handle.append(createFileHandleByLevel(_level))

for _handle in handle:
    logger.addHandler(_handle)
