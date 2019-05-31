'''
3号机器人

'''
import rconfig as rc
import copy


'''智能机器  类定义开始'''
 
class robot(object):
   

    def getKind(self):
        return 3

    def getName(self):
        return rc.robots_name[self.getKind()]

    def getPos(self,num,boardlist,player_number):
  
        row = column = len(boardlist)

        num1 = num2 = 0   #初始化黑棋和白棋的计数
        
        for i in range(row):
            for j in range(column):
                if boardlist[i][j]==1 :
                    num1 +=1
                elif boardlist[i][j]==2 :
                    num2 +=1

        if (num1==0) : return(row//2,column//2,9999) #棋盘正中落第一子

        if num1 > num2 : #该白棋下
            player_number = 1
            enemy_number = 2
        else : #该黑棋下
            player_number = 1
            enemy_number = 2

        max_score=0
        x = -1
        y = -1
        
        for i in range(row):
            for j in range(column):
                if boardlist[i][j]!=1 and boardlist[i][j]!=2:
                    my_score=one_score(boardlist,player_number,i,j)
                    enemy_score=one_score(boardlist,enemy_number,i,j)
                    score=my_score*2.5+enemy_score
                    if score>=max_score:
                        max_score=score
                        x=j
                        y=i
        
        return (x,y)
    
'''智能机器  类定义结束'''


#对当前位置的棋型打分,  0表示空格，1表示己方棋子，2表示敌方棋子
def point(tmpstr):
    
    base = [0,1,2,3,4,5] #棋子个数基数
    rank = 10  # 棋子个数幂底数

    if '11111' in tmpstr :   #五连
        return rank**base[5]*2   
    elif '011110' in tmpstr : #左右四
        return rank**base[4]*2  
    elif '0011100' in tmpstr : #左右三
        return rank**base[3]*2  
    elif '00011000' in tmpstr: #左右二
        return rank**base[2]*2  
    elif '000010000' in tmpstr: #左右一
        return rank**base[1]*2  
    elif '01111' in tmpstr or '11110' in tmpstr : # 单四
        return rank**base[4]
    elif '00111' in tmpstr or '11100' in tmpstr : # 单三
        return rank**base[3]
    elif '00011' in tmpstr or '11000' in tmpstr : # 单二
        return rank**base[2]
    elif '00001' in tmpstr or '10000' in tmpstr : # 单一
        return rank**base[1]
    else :
        return 0




#判断下在某一点的分数
def one_score(boardlist,player_number,i,j):
    score=0
    fake=copy.deepcopy(boardlist)#复制棋盘
    fake[i][j]=player_number#模拟落子
    #限定这次落子可能影响的范围
    up=max(i-5,0)
    down=min(i+5,rc.row-1)
    left=max(j-5,0)
    right=min(j+5,rc.column-1)
    #往4个角的长度
    leftup=min(j-left,i-up)
    leftdown=min(j-left,down-i)
    rightup=min(right-j,i-up)
    rightdown=min(right-j,down-i)

    u_d=l_r=lu_rd=ru_ld=''
    #将四个方向的棋子序列转化为字符串
    for k in range(up,down+1):#竖直方向
        u_d+=str(fake[k][j])
    for k in range(left,right+1):#水平方向
        l_r+=str(fake[i][k])
    for k in range(leftup,0,-1):#左上到右下
        lu_rd+=str(fake[i-k][j-k])
    for k in range(rightdown+1):
        lu_rd+=str(fake[i+k][j+k])
    for k in range(rightup,0,-1):
        ru_ld+=str(fake[i-k][j+k])#右上到左下
    for k in range(leftdown+1):
        ru_ld+=str(fake[i+k][j-k])

    #转化为point函数能处理的格式
    u_d=str_deal(u_d,player_number)
    l_r=str_deal(l_r,player_number)
    lu_rd=str_deal(lu_rd,player_number)
    ru_ld=str_deal(ru_ld,player_number)

    #计算总分数
    for k in (u_d,l_r,lu_rd,ru_ld):
        score+=point(k)
    return score


#将传入的字符串进行处理，等于number的数字转化为1,不等于的转化为2，其他转化为0
def str_deal(tmpstr,number):
    result=''
    for x in tmpstr:
        if x=='1' or x=='2':
            if x==str(number):
                result+='1'    #自己方子
            else:
                result+='2'    #敌方子或者墙壁
        else:
            result+='0'        #空位
    return result

