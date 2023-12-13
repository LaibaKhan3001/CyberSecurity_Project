import pymysql
from user import User
from contact import Contact
class DBHandler:
    def __init__(self,host,user,password,database):
        self.host=host
        self.user = user
        self.password=password
        self.database=database

    def register(self,username, password,email,age,height,religion,location,education,mStatus,gender):
        mydb = None
        mydbCursor=None
        inserted = False
        try:

            # Get DB Connection
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            sql = "insert into users(username, password,email,age,height,religion,location,education,mStatus,gender) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
            args = (username, password,email,age,height,religion,location,education,mStatus,gender)
            mydbCursor.execute(sql, args)
            mydb.commit()
            inserted=True
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return  inserted


    def checkUserExist(self,username):
        mydb = None
        mydbCursor=None
        exist = False
        try:
            # Get DB Connection
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            sql = "Select username from users where username=%s"
            args = (username)
            mydbCursor.execute(sql, args)
            row=mydbCursor.fetchone()
            if row !=None:
                exist=True

        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return  exist

    def checkUserExist2(self,username,password):
        mydb = None
        mydbCursor=None
        exist = False
        try:
            # Get DB Connection
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            sql = "Select username from users where username=%s and password=%s"
            args = (username,password)
            mydbCursor.execute(sql, args)
            row=mydbCursor.fetchone()
            if row !=None:
                exist=True

        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return  exist

    def view(self,username):
        mydb = None
        mydbCursor=None
        # Get DB Connection
        mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        # Get cursor object
        mydbCursor = mydb.cursor()
        sql = "Select * from users where username=%s"
        args = (username,)
        mydbCursor.execute(sql, args)
        row = mydbCursor.fetchone()
        user=User(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10])
        if mydbCursor != None:
            mydbCursor.close()
        if mydb != None:
            mydb.close()
        return user

    def matches(self,username):
        mydb = None
        mydbCursor=None
        user_list = []
        # Get DB Connection
        mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        # Get cursor object
        mydbCursor = mydb.cursor()
        sql = "Select * from users where username=%s"
        args = (username,)
        mydbCursor.execute(sql, args)
        row = mydbCursor.fetchone()
        gen=row[10]
        if gen=="female":
            sql = "Select * from users where gender=%s"
            gender="male"
            args = (gender,)
            mydbCursor.execute(sql, args)
            rows = mydbCursor.fetchall()
            for row in rows:
                user = User(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
                user_list.append(user)
        else:
            sql = "Select * from users where gender=%s"
            gender = "female"
            args = (gender,)
            mydbCursor.execute(sql, args)
            rows = mydbCursor.fetchall()
            for row in rows:
                user = User(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
                user_list.append(user)
        if mydbCursor != None:
            mydbCursor.close()
        if mydb != None:
            mydb.close()
        return user_list




    def search(self,gender,location,age_from,age_to,mStatus):
        mydb = None
        mydbCursor=None
        user_list = []
        # Get DB Connection
        mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        # Get cursor object
        mydbCursor = mydb.cursor()
        sql = "SELECT * FROM users WHERE gender=%s AND location=%s AND age >= %s AND age <= %s AND mStatus=%s"
        args = (gender, location, age_from, age_to, mStatus)
        mydbCursor.execute(sql, args)
        rows = mydbCursor.fetchall()
        for row in rows:
            user = User(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
            user_list.append(user)
        if mydbCursor != None:
            mydbCursor.close()
        if mydb != None:
            mydb.close()
        return user_list

    def contact(self,name, phone,email,message):
        mydb = None
        mydbCursor=None
        inserted = False
        try:

            # Get DB Connection
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            sql = "insert into contacts(name, phone,email,msg) values (%s,%s,%s,%s) "
            args = (name, phone,email,message)
            mydbCursor.execute(sql, args)
            mydb.commit()
            inserted=True
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return  inserted

    def contactShow(self):
        mydb = None
        mydbCursor=None
        contact_list = []
        # Get DB Connection
        mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        # Get cursor object
        mydbCursor = mydb.cursor()
        sql = "Select * from contacts"
        args = ()
        mydbCursor.execute(sql, args)
        rows = mydbCursor.fetchall()
        for row in rows:
            con = Contact(row[1], row[2], row[3], row[4])
            contact_list.append(con)
        if mydbCursor != None:
            mydbCursor.close()
        if mydb != None:
            mydb.close()
        return contact_list