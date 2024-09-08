
from data import DataStore
from .cameras import Cameras


class SQL:

    def __init__(self):
        self.sql = DataStore()

    def __del__(self):
        self.sql.close()



    def battery(self):
        return self.sql.batteryJSON()
