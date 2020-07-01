# qqmessageoutput
安卓QQ聊天记录导出/安卓QQ数据库解密

# Usage

```python
# 初始化
q = QQoutput(dbfile, key)
# 获得所有好友的个人资料
q.getAllMyFriends()
# 导出聊天记录
q.output(yourfriendqq, mode)
```

# Tips

获取db文件手机最好要root。但是当初经过我不屑的探索，没有root也不是没有办法。

在QQ官方更新了聊天记录备份功能之后，可以先将数据备份到电脑，然后再把数据导入到一个root过的设备（比如模拟器），再提取db文件。

获取db文件的方法请移步我写的文章：[安卓QQ聊天记录导出、备份完全攻略](https://www.cnblogs.com/roadwide/p/11220211.html)

```
data\data\com.tencent.mobileqq\databases\你的QQ.db
```
另外我还发现，如果聊天记录过多，会将较早的聊天记录存入以下数据库
```
data\data\com.tencent.mobileqq\databases\slowtable_你的QQ.db
```

yourkey是解密的密钥，一般是手机序列号，拨号键盘下输入`*#06#`

部分新版qq的解密密钥则可能位于以下文件中

```
data\data\com.tencent.mobileqq\files\kc
```

手机QQ的db文件加密方式是异或加密，如果找不到自己的key可以反向破解



**刚刚发现，QQ竟然支持手机聊天记录备份了！！！**

![QQmsg](./QQmsg.png)

# Update

[2019-10-02]新增了QQ群的消息记录导出，mode=1是好友，2是群

[2020-04-22]增加导出所有好友个人资料功能，优化代码（以前写的代码冗余太多，~~太烂了~~）

# ToDo

- [ ] 自行解密key功能
- [ ] 导出的聊天记录用不同颜色区分是“你”说的，还是“我”说的
- [ ] 导出的聊天记录用QQ-昵称-备注这样的形式，增加辨识度