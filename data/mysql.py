import MySQLdb
from .info import PiCamInfo


class MysqlStore:

    def __init__(self,database='picam',host='127.0.0.1',user='sql',password='sql'):
        self.db = MySQLdb.connect(database=database,host=host,user=user,password=password)



    @property
    def cameras(self):
        with self.db.cursor() as cursor:
            cursor.execute('select model FROM cameras ORDER BY idx')
            items = cursor.fetchall()
            return [item[0] for item in items]

    @cameras.setter
    def cameras(self,cams):
        entries = [(idx, cams[idx]) for idx in range(len(cams))]
        with self.db.cursor() as cursor:
            cursor.execute('DELETE FROM cameras')
            cursor.executemany("INSERT INTO cameras (idx, model) VALUES (%s, %s)", entries)



    @property
    def modes(self):
        with self.db.cursor() as cursor:
            cursor.execute('select camera, model, format, width, height, fps from modes join cameras on camera=idx')
            raw = cursor.fetchall()
            items = [PiCamInfo.fromTuple(row) for row in raw]
            return items

    @modes.setter
    def modes(self,modes):
        entries = [mode.tuple() for mode in modes]
        with self.db.cursor() as cursor:
            cursor.execute('DELETE FROM modes')
            cursor.executemany("INSERT INTO modes (camera, format, width, height, fps) VALUES (%s, %s, %s, %s, %s)", entries)




