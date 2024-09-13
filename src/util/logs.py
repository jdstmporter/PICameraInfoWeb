import logging
import logging.handlers
import enum
import traceback
from syslog import LOG_USER


class LogOutput(enum.Flag):
    SYSLOG = enum.auto()
    FILE = enum.auto()
    STDERR = enum.auto()

class LogOptions:
    Levels = {
        'debug': logging.DEBUG,
        'info' : logging.INFO,
        'warning' : logging.WARNING,
        'error' : logging.ERROR
    }

    def __init__(self,output = LogOutput.STDERR,**kwargs):
        self.opts = {
            'output' : output,
            'level' : kwargs.get('level', logging.INFO)
        }

        if LogOutput.FILE in output:
            self.opts['file'] = kwargs.get('file','/var/log/logfile')
        if LogOutput.SYSLOG in output:
            self.opts['facility'] = kwargs.get('facility',LOG_USER)

    def __getattr__(self,key):
        return self.opts[key]

    def __str__(self):
        lines = '\n'.join([f'    {k} : {v}' for k,v in self.opts.items()])
        return f'Logging options:\n{lines}'



class Logger:

    def __init__(self,name,options = LogOptions()):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(options.level)
        self.handlers = []

        if LogOutput.STDERR in options.output:
            self.handlers.append(logging.StreamHandler())
        if LogOutput.FILE in options.output:
            self.handlers.append(logging.FileHandler(options.file))
        if LogOutput.SYSLOG in options.output:
            self.handlers.append(logging.handlers.SysLogHandler(facility=options.facility))

        for handler in self.handlers:
            self.logger.addHandler(handler)

    def _log(self, level, message, *args, **kwargs):
        self.logger.log(level,message,*args,extra=kwargs)

    def exception(self,e):
        msg = f'{e}\n{traceback.format_exc()}'
        self._log(logging.CRITICAL,msg)

    def __getattr__(self, key):
        try:
            level = self.Levels[key]
            def fn(msg,*args,**kwargs):
                    self._log(level,msg,*args,**kwargs)
            return fn
        except Exception as e:
            self.logger.error('Error logging message',exc_info=e,extra=dict(level=key))

    @classmethod
    def make(cls,name=__name__,options=LogOptions()):
        cls.log = Logger(name,options=options)

Logger.make()




