"""
- 小智五子棋 -
人工智能博弈与决策课程
中科智芯 张磊 2019年5月
"""

import tkinter
import time
from tkinter import ttk  
from tkinter import scrolledtext  
from tkinter import Menu  
from tkinter import Spinbox  
from tkinter import messagebox as mBox
from sgfile import SGFflie


from tkinter.filedialog import askopenfilename
from tkinter import *

import time
import copy
import os
import sys
import rconfig as rc

class Stack(object):
    # 初始化栈为空列表
    def __init__(self):
        self.items = []

    # 判断栈是否为空,返回布尔值
    def is_empty(self):
        return self.items == []

    # 返回栈顶元素
    def top(self):
        return self.items[len(self.items) - 1]

    # 返回栈的大小
    def size(self):
        return len(self.items)

    # 把新的元素堆进栈里面
    def push(self, item):
        self.items.append(item)

    # 把栈顶元素丢出去
    def pop(self):
        item = self.items[len(self.items) - 1]
        del self.items[len(self.items) - 1]
        return item

    # 清空栈
    def clear(self):
        self.items = []


class Five(object):

    def __init__(self):
        
        self.IsStart = False
        self.num = 0   #当前的下棋步数  
        self.flag = 0   #胜方 0无，1黑胜，2白胜,3平
        self.cs = 0  # 0不显示数字，1显示数字
        self.boardlist = [[0 for i in range(rc.row)] for j in range (rc.column)]
        self.move_stack = Stack()
        self.window = Tk()
        self.ff = 0
        self.var = IntVar()
        self.var.set(0)
        self.var1 = IntVar()
        self.var1.set(0)
        self.var2 = IntVar()
        self.var2.set(0)
        self.window.title("小智五子棋【中科院计算所人工智能课程】")
        self.window.geometry("1000x800")
        self.window.resizable(0, 0)
        self.canvas=Canvas(self.window,width=19*40+20,height=19*40+20,bg='#ffcc99')#创建画布
        self.canvas.bind('<Button-1>',self.downQi) #绑定鼠标左键点击触发下棋事件
        self.canvas.bind_all('<BackSpace>',self.back) #绑定backspace键点击悔棋上一步  
        self.canvas.bind_all('<space>',self.ChangeShow) #绑定space键切换数字显示  
        self.draw_board()
        self.robot1 = None  #黑方
        self.robot2 = None  #白方
        self.canvas.grid(row=0, column=0)

        
        self.sgf = SGFflie()
        sys.setrecursionlimit(99999999)

    def draw_board(self):
        for i in range(rc.row):
            if i == 0 or i == rc.row-1:
                self.canvas.create_line((30, 30 + i * 40), (rc.row*40-10, 30 + i * 40), width=2)
            else:
                self.canvas.create_line((30, 30 + i * 40), (rc.row*40-10, 30 + i * 40), width=1)
        for j in range(rc.column):
            if j == 0 or j == rc.column-1:
                self.canvas.create_line((30 + j * 40, 30), (30 + j * 40, rc.row*40-10), width=2)
            else:
                self.canvas.create_line((30 + j * 40, 30), (30 + j * 40, rc.row*40-10), width=1)

        if rc.row!=19 or rc.column!=19:  #不是正规棋盘不画星
            return
        self.canvas.create_oval((3*40+26,3*40+26),(3*40+34,3*40+34),fill='#555555')#星
        self.canvas.create_oval((9*40+26,9*40+26),(9*40+34,9*40+34),fill='#555555')#星
        self.canvas.create_oval((15*40+26,15*40+26),(15*40+34,15*40+34),fill='#555555')#星
        self.canvas.create_oval((15*40+26,3*40+26),(15*40+34,3*40+34),fill='#555555')#星
        self.canvas.create_oval((9*40+26,3*40+26),(9*40+34,3*40+34),fill='#555555')#星
        self.canvas.create_oval((15*40+26,9*40+26),(15*40+34,9*40+34),fill='#555555')#星
        self.canvas.create_oval((3*40+26,9*40+26),(3*40+34,9*40+34),fill='#555555')#星
        self.canvas.create_oval((3*40+26,15*40+26),(3*40+34,15*40+34),fill='#555555')#星
        self.canvas.create_oval((9*40+26,15*40+26),(9*40+34,15*40+34),fill='#555555')#星


    def draw(self):   #画线，星和棋子
        self.draw_board()
        # 遍历栈后下棋
        slen = self.move_stack.size()
        for i in range(slen):
            temp = self.move_stack.items[i]
            #print(move_stack.items[i])
            b = temp[2]
            a = temp[1]

            if temp[3]==1:
                self.canvas.create_oval(((a)*40+16,(b)*40+16),((a+1)*40+4,(b+1)*40+4),fill='black')#黑棋
                if self.cs :
                    self.canvas.create_text(((a)*40+30,(b)*40+30),text=temp[0],fill = 'white')
            else:
                self.canvas.create_oval(((a)*40+16,(b)*40+16),((a+1)*40+4,(b+1)*40+4),fill='white')#白棋
                if self.cs :
                    self.canvas.create_text(((a)*40+30,(b)*40+30),text=temp[0],fill = 'black')

                
    def show(self): #每下一步都会重新绘制整个棋盘
        self.canvas.delete("all")
        self.draw()

        #绘制最后一颗AI下的棋子 brown
        if not self.move_stack.is_empty() :
            temp = self.move_stack.items[self.move_stack.size()-1]
            i = temp[2]
            j = temp[1]
            if i!=-1 and j!=-1 :
                self.canvas.create_oval(((j)*40+16,(i)*40+16),((j+1)*40+4,(i+1)*40+4), outline="brown")
        
        
    def downQi(self,event):#人类落子
        if self.flag==0 and self.IsStart :
            x=round((event.x-30)/40)
            y=round((event.y-30)/40)
            if self.boardlist[y][x]==0:
                self.num +=1
                if self.num%2==1 and self.robot1.getKind() == -1:  #人类下黑子   
                    self.down(x,y,1,-1)  

                elif self.num%2==0 and self.robot2.getKind() == -1:  #人类下白子    
                    self.down(x,y,2,-1)
                    
      
                
    def ChangeShow(self,event): #切换数字显示
        if self.cs == 0 :
            self.cs = 1
        else :
            self.cs = 0
        self.show()
        self.judge()
        

    def OpenFile(self):
        """打开保存好的棋谱"""
        
        file_path = askopenfilename(filetypes=(('sgf file', '*.sgf'),('All File', '*.*')))
        print(file_path)
        if len(file_path) == 0:
            return
        qipu = self.sgf.openfile(file_path)
        print(qipu)
        
        self.move_stack.clear()
        self.resetButton()

        self.label["text"]="已成功载入\n历史棋谱"
        slen = len(qipu)
        if slen % 2 == 0 :
            self.flag = 2
        else :
            self.flag = 1
        for i in range(slen):
            item = [int(qipu[i][3]),int(qipu[i][0]),int(qipu[i][1]),int(qipu[i][2]+1),-99]
            self.move_stack.push(item)
        self.show()
        

        

    def SaveFile(self, method=1):
        """保存棋谱"""    
        qipu = []
        
        slen = self.move_stack.size()
        for i in range(slen):
            temp = self.move_stack.items[i]
            print(temp)
            if i % 2==0:
                qipu.append([temp[1],temp[2],0,i+1])
            else:
                qipu.append([temp[1],temp[2],1,i+1])
                
        self.sgf.savefile(self.robot1.getName()+"vs"+self.robot2.getName(),qipu)
        self.label["text"]="已成功保存\n本盘棋谱"
                
    def back(self,event):#悔棋 暂时注销
        pass 
        
    def showSucess(self): #画成线的五子棋
        temp = self.move_stack.items[self.move_stack.size()-1]
        b = temp[2]
        a = temp[1]
        color = "red"
        x=self.boardlist[b][a]
        if self.ff == 1:  #竖直
            for k in range(0,5): #向上
                if b-k<0 or self.boardlist[b-k][a] != x :
                    break
                self.canvas.create_oval(((a)*40+16,(b-k)*40+16),((a+1)*40+4,(b-k+1)*40+4), outline=color)
            for k in range(0,5): #向下
                if b+k>18 or self.boardlist[b+k][a] != x :
                    break
                self.canvas.create_oval(((a)*40+16,(b+k)*40+16),((a+1)*40+4,(b+k+1)*40+4), outline=color)     
                    
        if self.ff == 2:   #水平
            for k in range(0,5): #向左
                if a-k<0 or self.boardlist[b][a-k] != x :
                    break
                self.canvas.create_oval(((a-k)*40+16,(b)*40+16),((a-k+1)*40+4,(b+1)*40+4), outline=color)
            for k in range(0,5): #向右
                if a+k>18 or self.boardlist[b][a+k] != x :
                    break
                self.canvas.create_oval(((a+k)*40+16,(b)*40+16),((a+k+1)*40+4,(b+1)*40+4), outline=color)     
             
        if self.ff == 3:   #左上至右下
            for k in range(0,5): #向左上
                if a-k<0 or b-k<0 or self.boardlist[b-k][a-k] != x :
                    break
                self.canvas.create_oval(((a-k)*40+16,(b-k)*40+16),((a-k+1)*40+4,(b-k+1)*40+4), outline=color)
            for k in range(0,5): #向右下
                if a+k>18 or b+k>18 or self.boardlist[b+k][a+k] != x :
                    break
                self.canvas.create_oval(((a+k)*40+16,(b+k)*40+16),((a+k+1)*40+4,(b+k+1)*40+4), outline=color)     
             
        if self.ff == 4:  #右上至左下
            for k in range(0,5): #向右上
                if a+k>18 or b-k<0 or self.boardlist[b-k][a+k] != x :
                    break
                self.canvas.create_oval(((a+k)*40+16,(b-k)*40+16),((a+k+1)*40+4,(b-k+1)*40+4), outline=color)
            for k in range(0,5): #向左下
                if b+k>18 or a-k<0 or self.boardlist[b+k][a-k] != x :
                    break
                self.canvas.create_oval(((a-k)*40+16,(b+k)*40+16),((a-k+1)*40+4,(b+k+1)*40+4), outline=color)     
             

        #判断某一点连子数目
    def many(self,n,i,j):
    
        if not(self.boardlist[i][j]==n):#判断是否是该棋子
            return 0
        else:
            n1=n2=n3=n4=1
            a=i
            b=j
            for k in range(5):#竖直
                x=self.boardlist[a][b]
                a+=1
                if a>rc.column-1:
                    break
                if x==self.boardlist[a][b]:
                    n1+=1
                else:
                    break
            a=i
            b=j 
            for k in range(5):#水平
                x=self.boardlist[a][b]
                b+=1
                if b>rc.row-1:
                    break
                if x==self.boardlist[a][b]:
                    n2+=1
                else:
                    break
            a=i
            b=j
            for k in range(5):#左上到右下
                x=self.boardlist[a][b]
                a+=1
                b+=1
                if a>rc.column-1 or b>rc.row-1:
                    break
                if x==self.boardlist[a][b]:
                    n3+=1
                else:
                    break
            a=i
            b=j
            for k in range(5):#右上到左下
                x=self.boardlist[a][b]
                a+=1
                b-=1
                if a>rc.column-1 or b<0:
                    break
                if x==self.boardlist[a][b]:
                    n4+=1
                else:
                    break
            if n1==5:
                self.ff = 1
            elif n2==5:
                self.ff = 2
            elif n3==5:
                self.ff = 3
            elif n4==5:
                self.ff = 4
            
        return max(n1,n2,n3,n4)
    
    def judge(self):
        for i in range(0,rc.row):
            for j in range(0, rc.column):
                how_many=self.many(1,i,j)
                if how_many==5:
                    self.flag=1
                    self.showSucess()
                    
                    self.label["text"]=self.robot1.getName()+"\n持黑第"+str(self.num)+"手胜!"
                   
                    return 
                how_many=self.many(2,i,j)
                if how_many==5:
                    self.flag=2
                    self.showSucess()
                    self.label["text"]=self.robot2.getName()+"\n持白第"+str(self.num)+"手胜!"
                   
                    
                    return

        n=0#棋盘上的棋子数量
        for i in range(0,rc.row):
            for j in range(0,rc.column):
                if(self.boardlist[i][j]==1 or self.boardlist[i][j]==2):
                    n=n+1
        
        if n==rc.column*rc.row:
            self.flag=3
            print("平局")
            self.label["text"]= "双方打平！"

    def reTrain(self):
        '''
        下一版本加入功能
        CNN 卷积神经网络 进行深度学习训练
        透过大量的保存的棋谱文件自己找出对应的逻辑与抽象概念。
        ''' 

    def resetButton(self):
        """重置按钮的回调函数，实现了整个棋盘重置"""
        self.flag = 0
        self.ff = 0
        self.IsStart = False
        self.cs=0  # 0不显示数字，1显示数字
        self.robot1 = None  #黑方
        self.robot2 = None  #白方
        self.num = 0 #下棋步数  
        
        for i in range(rc.row):
            for j in range(rc.column):
                self.boardlist[i][j]=0
        
        self.move_stack.clear()
        self.b0['state'] = 'normal'
        self.player1Chosen['state'] = 'normal'
        self.player2Chosen['state'] = 'normal'
        self.label["text"] = "请选择双方对手后\n点击[开始下棋]"
        self.canvas.delete("all")
        self.draw_board()
        self.canvas.grid(row=0, column=0)

    def startButton(self):
        if self.IsStart == False:
            self.IsStart = True
            self.b0['state'] = 'disabled'
            self.player1Chosen['state'] = 'disabled'
            self.player2Chosen['state'] = 'disabled'
            
            if self.flag != 0:
                self.resetButton()
            self.robot1 = rc.getRobot(self.player1Chosen.get())
            self.robot2 = rc.getRobot(self.player2Chosen.get())

            print("========" + self.robot1.getName() + " VS " + self.robot2.getName() + "========")
            
            if self.flag == 0 : # 棋局未结束
                if self.num%2==0 :  #第一步
                    self.aiBlackChess()
                else:
                    self.aiWhiteChess()
  
    def aiBlackChess(self):
        
         if self.flag ==0:  #棋局未结束
            if self.robot1.getKind() == -1: return #该人类下 直接退出
            self.num += 1
            x,y,score=self.robot1.getPos(self.num,self.boardlist,1)#查找最优位置
            self.down(x,y,1,score) #落子
        

    def aiWhiteChess(self):
        if self.flag ==0:  #棋局未结束
            if self.robot2.getKind() == -1: return #该人类下 直接退出
            self.num += 1
            x,y,score=self.robot2.getPos(self.num,self.boardlist,2)#查找最优位置
            self.down(x,y,2,score) #落子
       

    def down(self,x,y,bw,score): #下棋并压入新的棋入栈

        if (self.boardlist[y][x]!=0) or (x > rc.row-1) or (x < 0) or (y>rc.column-1) or (y<0 ): #犯规
            self.flag=3
            print(x,y,self.boardlist[y][x])
            print(str(self.num)+" 违例，直接判负 ["+str(x)+","+str(y)+"] 分数 "+str(score))
            if bw == 1:
                self.label["text"] = self.robot1.getName() + "\n违例，直接判负"
            else :
                self.label["text"] = self.robot2.getName() + "\n违例，直接判负"
            return 
        self.move_stack.push([self.num,x,y,bw,score])   
        self.boardlist[y][x]=bw
        self.show()
        if bw == 1:
            print(str(self.num)+" "+self.robot1.getName()+" 黑棋 ["+str(x)+","+str(y)+"] 分数"+str(score))
            self.label["text"] = "第"+str(self.num)+"手黑棋\n横"+str(x)+"竖"+str(y)
        else :
            print(str(self.num)+" "+self.robot2.getName()+" 白棋 ["+str(x)+","+str(y)+"] 分数"+str(score))
            self.label["text"] = "第"+str(self.num)+"手白棋\n横"+str(x)+"竖"+str(y)  
        self.judge()
        self.canvas.update()  #0.3秒后立刻更新画布
        self.canvas.after(300)
        
        if self.flag == 0: #棋局没有结束，继续下
            if bw == 1 :
                self.aiWhiteChess()
            else :
                self.aiBlackChess()
        



        
    def showButton(self):
        """开始，主要实现一些按钮与按键"""
        label1=ttk.Label(self.window, text="黑棋方:")
        label1.place(relx=0, rely=0, x=800, y=50)
        number1 = StringVar()
        self.player1Chosen = ttk.Combobox(self.window, width=10, textvariable=number1)
        self.player1Chosen['values'] = rc.robots_name    # 设置下拉列表的值
        self.player1Chosen.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
        self.player1Chosen.place(relx=0, rely=0, x=850, y=50)

        label2=ttk.Label(self.window, text="白棋方:")
        label2.place(relx=0, rely=0, x=800, y=100)
        number2 = StringVar()
        self.player2Chosen = ttk.Combobox(self.window, width=10, textvariable=number2)
        self.player2Chosen['values'] = rc.robots_name      # 设置下拉列表的值
        self.player2Chosen.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
        self.player2Chosen.place(relx=0, rely=0, x=850, y=100)


     
        self.b0 = Button(self.window, text="  开 始 下 棋  ", command=self.startButton)
        self.b0.place(relx=0, rely=0, x=835, y=150)

        b1 = Button(self.window, text="  重 置 游 戏  ", command=self.resetButton)
        b1.place(relx=0, rely=0, x=835, y=200)

        self.label = Label(self.window, text="请选择双方对手\n点[开始下棋]", background="#EEEEEE", font="黑体")
        self.label.place(relx=0, rely=0, x=835, y=300)    

  
        b3 = Button(self.window, text="  开 始 训 练  ", command=self.reTrain ,state="disabled")
        b3.place(relx=0, rely=0, x=835, y=400)
        
        b3 = Button(self.window, text="  打 开 棋 谱  ", command=self.OpenFile)
        b3.place(relx=0, rely=0, x=835, y=450)
 
        b4 = Button(self.window, text="  保 存 棋 谱  ", command=self.SaveFile)
        b4.place(relx=0, rely=0, x=835, y=500)

        info = Label(self.window, text=":::游戏说明:::\n\n\
人类点鼠标左键下棋\n空格键切换数字显示\n\n\
下棋过程可保存棋谱\n机器学习可反复训练",padx=0, pady=5, bd=6, font="黑体")
        info.place(relx=0, rely=0, x=800, y=590)

        self.window.mainloop()

if __name__ == '__main__':
    game = Five()
    game.showButton()

    del game
