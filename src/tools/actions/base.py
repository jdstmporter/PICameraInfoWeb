
class BaseAction:

    def __init__(self):
        pass

    def __call__(self,**kwargs):
        pass

class ToolAction(BaseAction):

    def __init__(self,name):
        super().__init__()
        self.name=name

    def list(self):
        pass

    def read(self):
        pass

    def write(self):
        pass

    def __call__(self,*args,**kwargs):
        action=kwargs['action']
        if action == 'raw':
            self.list()
        elif action == 'load':
            self.read()
        elif action == 'store':
            self.write()
        else:
            raise Exception(f'Unknown action {action} on {self.name} tool processor')
