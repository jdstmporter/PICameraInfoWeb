
import MySQLdb

class MysqlStore:

    def __init__(self,database='picam',host='127.0.0.1',user='sql',password='sql'):
        self.db = MySQLdb.connect(database=database,host=host,user=user,password=password)
        self.cursor = self.db.cursor()

    def _tx(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(f'Error : {e}')
            self.db.rollback()

    def close(self):
        self.cursor.close()

    def select(self,sql):
        print(sql)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def clean(self,mode):
        sql = mode.deleteSQL()
        print(sql)
        self._tx(sql)

    def write(self,mode,data,clean=True):
        if clean:
            self.clean(mode)
        sql=mode.insertSQL(data)
        print(sql)
        self._tx(sql)


    def read(self,mode):
        sql=mode.readSQL()
        print(sql)
        self.cursor.execute(sql)
        if mode.single():
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()

