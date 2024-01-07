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
