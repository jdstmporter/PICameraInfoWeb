
from data import MysqlStore
from .base import display, getInformation

def dumpDB():
    try:
        mysql = MysqlStore()
        display(mysql.cameras ,mysql.modes)
        mysql.close()
    except Exception as e:
        print(f'Error : {e}')


def initialiseDB():
    try:
        print('Initialising camera info database')
        print('Getting camera info')
        cameras, modes = getInformation()
        display(cameras, modes)


        print('Loading database')
        mysql = MysqlStore()
        mysql.setCameras(cameras)
        mysql.setModes(modes)
        mysql.close()
    except Exception as e:
        print(f'Error: {e}')