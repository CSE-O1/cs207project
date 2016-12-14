import psycopg2
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class postgresAPI:
    """
    postgresAPI to create tabel and query in database
    """

    def __init__(self, host, dbname, user, password, table):
        self._host = host
        self._dbname = dbname
        self._user = user
        self._password = password
        self._table = table
        self._cursor = self.connect()

    def connect(self):
        """
        connect to database
        """
        conn_string = "host=%s dbname=%s user=%s password=%s" % (self._host, self._dbname, self._user, self._password)
        try:
            self._conn = psycopg2.connect(conn_string)
        except:
            print("unable to connect to the database")
        self._cursor = self._conn.cursor()
        print('%s connected!' % self._dbname)
        return self._cursor

    def create(self):
        """
        create a table
        """
        tmp1 = "CREATE TABLE %s (id INT PRIMARY KEY,mean FLOAT(5),std FLOAT(5),blarg FLOAT(5),level VARCHAR (20));" % (
            self._table)
        self._cursor.execute(tmp1)
        # Make the changes to the database persistent
        self._conn.commit()

    def insert(self, data):
        """
        insert an entry with metadata [id, mean, std, blarg, level]
        """
        # input as a list
        tmp2 = "INSERT INTO %s VALUES (%d,%f,%f,%f,'%s');" % (
            self._table, int(data[0]), float(data[1]), float(data[2]), float(data[3]), str(data[4]))
        self._cursor.execute(tmp2)
        # Make the changes to the database persistent
        self._conn.commit()

    def query_id(self, ID):
        """
        query id in a list [id1, id2, id3...]
        """
        ID_str = str(", ".join(str(x) for x in ID))
        tmp3 = "SELECT * FROM %s WHERE %s in (%s);" % (self._table, 'id', ID_str)
        self._cursor.execute(tmp3)
        records = self._cursor.fetchall()
        return records

    def query_mean_range(self, mean_range):
        """
        query mean in a range [lower bound, upper bound]
        """
        tmp4 = "SELECT * FROM %s WHERE %s > %s AND %s < %s;" % (
            self._table, 'mean', mean_range[0], 'mean', mean_range[1])
        self._cursor.execute(tmp4)
        records = self._cursor.fetchall()
        return records

    def query_std_range(self, std_range):
        """
        query std in a range [lower bound, upper bound]
        """
        tmp5 = "SELECT * FROM %s WHERE %s > %s AND %s < %s;" % (self._table, 'std', std_range[0], 'std', std_range[1])
        self._cursor.execute(tmp5)
        records = self._cursor.fetchall()
        return records

    def query_blarg_range(self, blarg_range):
        """
        query blarg in a range [lower bound, upper bound]
        """
        tmp6 = "SELECT * FROM %s WHERE %s > %s AND %s < %s;" % (
            self._table, 'blarg', blarg_range[0], 'blarg', blarg_range[1])
        self._cursor.execute(tmp6)
        records = self._cursor.fetchall()
        return records

    def query_level(self, level_vals):
        """
        query level in a list [level1, level2, level3...]
        """
        level_str = str("', '".join(str(x) for x in level_vals))
        tmp7 = "SELECT * FROM %s WHERE %s in ('%s');" % (self._table, 'level', level_str)
        self._cursor.execute(tmp7)
        records = self._cursor.fetchall()
        return records

    def query_all(self):
        """
        query all entries in the table
        """
        tmp8 = "SELECT * FROM %s;" % (self._table)
        self._cursor.execute(tmp8)
        records = self._cursor.fetchall()
        return records

    def close(self):
        """
        close connection to database
        """
        # Close communication with the database
        self._cursor.close()
        self._conn.close()
