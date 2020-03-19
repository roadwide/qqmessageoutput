from _overlapped import NULL
import hashlib
import sqlite3
import time
import os


class QQoutput():
    def __init__(self, db, key):
        self.key = key  # 解密用的密钥
        self.c = sqlite3.connect(db).cursor()

    # msgdata mode=0
    # other mode=1
    def fix(self, data, mode):
        if(mode == 0):
            rowbyte = []
            for i in range(0, len(data)):
                rowbyte.append(data[i] ^ ord(self.key[i % len(self.key)]))
            rowbyte = bytes(rowbyte)
            try:
                msg = rowbyte.decode(encoding='utf-8')
            except:
                msg = NULL
            return msg
        elif(mode == 1):
            str = ''
            try:
                for i in range(0, len(data)):
                    str += chr(ord(data[i]) ^ ord(self.key[i % len(self.key)]))
            except:
                str = NULL
            return str

    def message(self, table_name):
        execute = f'select msgData,senderuin,time from {table_name}'
        cursor = self.c.execute(execute)
        allmsg = []
        for row in cursor:
            msgdata = row[0]
            uin = row[1]
            ltime = time.localtime(row[2])

            sendtime = time.strftime("%Y-%m-%d %H:%M:%S", ltime)
            msg = self.fix(msgdata, 0)
            senderuin = self.fix(uin, 1)

            amsg = []
            amsg.append(sendtime)
            amsg.append(senderuin)
            amsg.append(msg)
            allmsg.append(amsg)
        return allmsg

    def output(self, dbfile):
        execute = f"SELECT name FROM sqlite_master WHERE type ='table' AND (name LIKE 'mr_friend_%' OR name LIKE 'mr_troop_%') ;"
        rows = self.c.execute(execute)
        lst_table_name = []
        for row in rows:
            # row[0] like mr_friend_{QQ号的MD5的16进制的字母大写}_New
            lst_table_name.append(row[0])

        dir_name = f'{dbfile}.dir'

        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        for table_name in lst_table_name:

            file = dir_name+'\\' + table_name+".html"
            f2 = open(file, 'w', encoding="utf-8")
            f2.write(
                "<head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /></head>")
            allmsg = self.message(table_name)
            for msg in allmsg:
                if msg[2] != 0:
                    try:
                        f2.write("<font color=\"blue\">")
                        f2.write(msg[0])
                        f2.write("</font>-----<font color=\"green\">")
                        f2.write(msg[1])
                        f2.write("</font></br>")
                        f2.write(msg[2])
                        f2.write("</br></br>")
                    except:
                        pass


if __name__ == "__main__":
    # config
    # 储存QQ聊天信息的db文件，qq号.db 或者是 slowtable_qq号.db,记得把文件和py代码放在同目录
    dbfile = ''
    # 解密的key,一般为IMEI,在files/IMEI文件
    key = ''

    q = QQoutput(dbfile, key)
    q.output(dbfile)
