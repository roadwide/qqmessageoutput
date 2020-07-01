from _overlapped import NULL
import hashlib
import sqlite3
import time


class QQoutput():
    # 初始化解密key，并连接sqlite3数据库
    def __init__(self, db, key):
        self.key = key  # 解密用的密钥
        self.c = sqlite3.connect(db).cursor()

    # 解密数据，针对不同数据用不同的方法
    def fix(self, data, mode):
        # msgdata mode=0
        # other mode=1
        if (mode == 0):
            rowbyte = []
            # 这么做是为了解决汉字的utf-8是三字节
            for i in range(0, len(data)):
                rowbyte.append(data[i] ^ ord(self.key[i % len(self.key)]))
            rowbyte = bytes(rowbyte)
            try:
                msg = rowbyte.decode(encoding='utf-8')
            except:
                msg = NULL
            return msg
        elif (mode == 1):
            str = ''
            try:
                for i in range(0, len(data)):
                    str += chr(ord(data[i]) ^ ord(self.key[i % len(self.key)]))
            except:
                str = NULL
            return str

    # 获得聊天记录
    def message(self, num, mode):
        # mode=1 friend
        # mode=2 troop
        num = str(num).encode('utf-8')
        md5num = hashlib.md5(num).hexdigest().upper()
        if (mode == 1):
            execute = "select msgData,senderuin,time from mr_friend_{md5num}_New".format(md5num=md5num)
        elif (mode == 2):
            execute = "select msgData,senderuin,time from mr_troop_{md5num}_New".format(md5num=md5num)
        else:
            print("error mode")
            exit(1)
        cursor = self.c.execute(execute)
        allmsg = []
        for row in cursor:
            msgdata, uin, ltime = row[0], row[1], time.localtime(row[2])

            sendtime = time.strftime("%Y-%m-%d %H:%M:%S", ltime)
            msg = self.fix(msgdata, 0)
            senderuin = self.fix(uin, 1)

            print([sendtime, senderuin, msg])
            allmsg.append([sendtime, senderuin, msg])
        return allmsg

        # 输出到文件

    # 导出聊天记录
    def output(self, num, mode):
        file = str(num) + ".html"
        f2 = open(file, 'w', encoding="utf-8")
        f2.write("<head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /></head>")
        allmsg = self.message(num, mode)
        for msg in allmsg:
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

    # 获得所有好友昵称，备注，QQ等数据,包括临时会话的人以及一些不知道哪来的人
    def getAllMyFriends(self):
        FriendsData = []
        # uin-QQ号，remark-备注，name-昵称
        execute = "select uin,remark,name from Friends"
        cursor = self.c.execute(execute)
        with open("FriendsData.txt", "w+", encoding="utf-8") as f:
            for i in cursor:
                uin, remark, name = i[0], i[1], i[2]

                decode_uin = self.fix(uin, 1)
                decode_remark = self.fix(remark, 1)
                decode_name = self.fix(name, 1)

                print("QQ:{}\t备注:{}\t昵称:{}".format(decode_uin, decode_remark, decode_name), file=f)
                FriendsData.append([decode_uin, decode_remark, decode_name])
        return FriendsData


# config
# 储存QQ聊天信息的db文件，以你的QQ号命名
dbfile = 'yourdb.db'
# 解密的key
key = ''
# 导出模式，1是好友，2是群
mode = 1
# 导出的聊天对象
yourfriendqq = 123456

# 初始化
q = QQoutput(dbfile, key)
# 获得所有好友的个人资料
q.getAllMyFriends()
# 导出聊天记录
q.output(yourfriendqq, mode)
