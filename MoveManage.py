import hashlib
import os
import sqlite3
from tkinter import *
import addMove


class MoveManage:
    __doc__ = "管理影片"

    def __init__(self):

        root=Tk()
        root.title="影片管理"

        b_addMove = Button(root, text="添加影片")
        b_addMove.grid(row=0, column=1, stick=W)
        b_addMove.bind("<Button-1>", self.addMove)

        b_updateView=Button(root,text="更新已有影片")
        b_updateView.grid(row=1, column=1, stick=W)
        b_updateView.bind("<Button-1>", self.updateDatebase)

        b_show = Button(root, text="显示存储库", command=self.Show)
        b_show.grid(row=2, column=1, stick=W)

        b_isSend=Button(root, text="查看已经传送过的", command=self.isSend)
        b_isSend.grid(row=3, column=1, stick=W)

        self.c = Label(root, text="")
        self.c.grid(row=4,column=1)

        root.mainloop()

    def isSend(self):
        sql="select * from isSend"
        re=self.sql_check(sql)

        ShowView = Tk()
        ShowView.title = "已发送过的影片列表"

        showStr=""
        for i in re:
            showStr=showStr+re[0]+"\n"

        c1 = Label(ShowView, text=showStr)
        c1.grid(row=0, column=0)

        l = Label(ShowView, text="影片名:")
        l.grid(row=1, column=0, sticky=W)

        # global e1
        self.e1 = Entry(ShowView)
        self.e1.grid(row=1, column=1, sticky=E)

        bl = Button(ShowView, text="添加已经传送完成的", command=self.sendadd)
        bl.grid(row=2, column=1, stick=W)

        bl = Button(ShowView, text="修改为不喜欢", command=self.sendaddBad)
        bl.grid(row=2, column=1, stick=W)

        self.c = Label(ShowView, text="")
        self.c.grid(row=3, column=1)

        ShowView.mainloop()

    def sendaddBad(self):
        try:
            s1 = self.e1.get()

            sql = "update isSend set MoveLikeID=3 where ID=\""+str(s1)+"\""

            re=self.sql_add(sql)

            self.c["text"] = "sessful"
        except:
            self.c["text"] = "error"

    def sendadd(self):
        try:
            s1 = self.e1.get()

            sql = "INSERT INTO \"MoveList\" (\"MoveName\", \"MoveLikeID\") VALUES (?,?)"
            para = (s1, "1")

            self.sql_add(sql, para)

            self.c["text"] = "sessful"
        except:
            self.c["text"] = "error"

    def getShow(self,sign):
        sql="select * from MoveList where MoveLikeID=\""+str(sign)+"\""
        re=self.sql_check(sql)
        # print(re)
        return re

    def Show(self):
        ShowView = Tk()
        ShowView.title="影片列表"


        movelist = self.getShow(1)
        if movelist.__len__()!=0:
            c1 = Label(ShowView, text="喜欢且已存储的：")
            c1.grid(row=0, column=0)
            showstr=""
            for i in movelist:
                showstr=showstr+i[0]+"\n"
            c1 = Label(ShowView, text=showstr)
            c1.grid(row=0, column=1)


        movelist = self.getShow(2)
        if movelist.__len__() != 0:
            c1 = Label(ShowView, text="喜欢但未存储的：")
            c1.grid(row=1, column=0)
            showstr = ""
            for i in movelist:
                showstr = showstr + i[0] + "\n"
            c1 = Label(ShowView, text=showstr)
            c1.grid(row=1, column=1)

        movelist = self.getShow(3)
        if movelist.__len__() != 0:
            c1 = Label(ShowView, text="不喜欢的：")
            c1.grid(row=2, column=0)
            showstr = ""
            for i in movelist:
                showstr = showstr + i[0] + "\n"
            c1 = Label(ShowView, text=showstr)
            c1.grid(row=2, column=1)


        movelist = self.getShow(4)
        if movelist.__len__() != 0:
            c1 = Label(ShowView, text="希望观看的：")
            c1.grid(row=3, column=0)
            showstr = ""
            for i in movelist:
                showstr = showstr + i[0] + "\n"
            c1 = Label(ShowView, text=showstr)
            c1.grid(row=3, column=1)

        ShowView.mainloop()


    def updateDatebase(self,event):
        self.c["text"] = "正在搜索文件，请稍后"
        self.FileList = []  # 存文件名
        self.FileTool = os.path.dirname(os.path.realpath(__file__))+"\\move"  # 存当前路径
        print(self.FileTool)
        # self.FileTool="X:/其他分区/ZZZZZZZZZZ"

        self.getFileList(self.FileTool)

        pathLen=len(self.FileTool)

        for i in range(len(self.FileList)):
           self.FileList[i]=str(self.FileList[i][pathLen+1:-4]).upper()

        for i in self.FileList:
            try:
                self.c["text"] = "正在添加" + i
                sql = "INSERT INTO \"MoveList\" (\"MoveName\", \"MoveLikeID\") VALUES (?,?)"
                para = (i,"1")
                self.sql_add(sql, para)

            except:
                pass

            finally:
                self.c["text"] = '添加完成'
        print(self.FileList)


    def sql_add(self, sql, para):#sql语句
        conn = sqlite3.connect("Move.sqlite3")
        cursor = conn.cursor()
        re=cursor.execute(sql, para)
        conn.commit()
        cursor.close()
        conn.close()

    def sql_check(self,sql):
        conn = sqlite3.connect("Move.sqlite3")
        cursor = conn.cursor()
        result = cursor.execute(sql)
        re = result.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return re



    def addMove(self,event):#添加影片窗口
        addMoveView=Tk()

        l = Label(addMoveView, text="影片名:")
        l.grid(row=0, column=0, sticky=W)

        # global e1
        self.e1 = Entry(addMoveView)
        self.e1.grid(row=0, column=1, sticky=E)

        bl = Button(addMoveView, text="添加想要看的", command=self.add4)
        bl.grid(row=1, column=1, stick=W)

        bl = Button(addMoveView, text="添加不喜欢的", command=self.add3)
        bl.grid(row=3, column=1, stick=W)

        self.c = Label(addMoveView, text="")
        self.c.grid(row=4)

        addMoveView.mainloop()



    def add4(self):#待尝试
        try:
            s1 = self.e1.get()

            sql="INSERT INTO \"MoveList\" (\"MoveName\", \"MoveLikeID\") VALUES (?,?)"
            para=(s1,"4")

            self.sql_add(sql,para)

            self.c["text"]="sessful"
        except:
            self.c["text"] = "error"




    def add3(self):#添加不喜欢
        try:
            s1=self.e1.get()
            try:#插入
                sql = "INSERT INTO \"MoveList\" (\"MoveName\", \"MoveLikeID\") VALUES (?,?)"
                para = (s1, "3")

                self.sql_add(sql, para)
            except:#更新
                sql="update  MoveList set MoveLikeID='3' where MoveName=(?)"
                para=(s1)
                self.sql_add(sql, para)
            finally:
                self.c["text"] = "sessful"
        except:
            self.c["text"] = "error"



    def add2(self):#添加喜欢但未存储的
        try:
            s1 = self.e1.get()
            try:
                sql = "INSERT INTO \"MoveList\" (\"MoveName\", \"MoveLikeID\") VALUES (?,?)"
                para = (s1, "2")

                self.sql_add(sql, para)
            except:
                sql="update  MoveList set MoveLikeID='2' where MoveName=(?)"
                para=(s1)
                self.sql_add(sql, para)
            finally:
                self.c["text"] = "sessful"
        except:
            self.c["text"] = "error"


    def mdavMD5(self, path):#计算MD5
        md5file = open(path, 'rb')
        md5 = hashlib.md5(md5file.read()).hexdigest()
        md5file.close()
        print(md5)
        return md5

    def getFileList(self,path):#获取目录
        path = path.replace("\\", "/")
        mlist = os.listdir(path)  # 获取目录下的所有文件
        for m in mlist:
            try:
                mpath = os.path.join(path, m)
                if os.path.isfile(mpath):
                    pt = os.path.abspath(mpath)
                    if pt not in self.FileList:
                        self.FileList.append(pt)
                    # print("  " + pt)
                else:
                    pt = os.path.abspath(path)
                    # print("  " + pt)
                    self.getFileList(pt)
            except:
                pass


if __name__ == '__main__':
    a=MoveManage()
    pass
