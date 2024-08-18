import os.path

from ..logs import SysLog

class FileOut:

    def __init__(self,name='info.json',path='/var/lib/picam'):
        self.name=name
        self.path=path
        self.fname=os.path.join(self.path,self.name)

    def write(self,obj):
        try:
            with open(self.fname,'w') as fp:
                fp.write(obj)
        except Exception as e:
            SysLog.error(str(e))

    def read(self):
        try:
            with open(self.fname, 'r') as fp:
                return fp.read()
        except Exception as e:
            SysLog.error(str(e))





