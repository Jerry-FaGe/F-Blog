import hashlib
import uuid

def getMd5(strs):
    h1 = hashlib.md5()
    h1.update(strs.encode(encoding='utf-8'))
    return h1.hexdigest()

def getUUID():
    return str(uuid.uuid4())