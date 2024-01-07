# uncompyle6 version 3.9.0
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: .\betterReticleSize-src\scripts\client\gui\mods\jakLibrary\util.py
# Compiled at: 2023-12-31 00:52:00
import ResMgr

class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def parseLangFields(langFile):
    """split items by lines and key value by ':'
        like yaml format"""
    result = {}
    langData = readFromVFS(langFile)
    if langData:
        for item in langData.splitlines():
            if ': ' not in item:
                continue
            key, value = item.split(': ', 1)
            result[key] = value

    return result


def readFromVFS(path):
    """using for read files from VFS"""
    fileInst = ResMgr.openSection(path)
    if fileInst is not None and ResMgr.isFile(path):
        return str(fileInst.asBinary)
    else:
        return
        return
# okay decompiling C:\dev\wot-mods\betterReticleSize-src\scripts\client\gui\mods\jakLibrary\util.pyc
