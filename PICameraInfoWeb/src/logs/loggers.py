import logging

class BaseLogger:

    def __init__(self, name=None, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

    def debug(self,message):
        self.logger.debug(message)
    def info(self,message):
        self.logger.info(message)
    def warning(self,message):
        self.logger.warning(message)
    def error(self, message):
        self.logger.info(message)

class SystemLogger(BaseLogger):

    def __init__(self,name=None,level=logging.INFO,filename='/var/log/cameras.log'):
        super().__init__(name,level)
        self.handler = logging.FileHandler(filename)
        self.logger.addHandler(self.handler)

class StderrLogger(BaseLogger):
    def __init__(self,name=None,level=logging.INFO,filename='/var/log/cameras.log'):
        super().__init__(name,level)
        self.handler = logging.StreamHandler()
        self.logger.addHandler(self.handler)