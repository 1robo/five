'''
1号机器人

'''
import copy


'''智能机器  类定义开始'''
 
class robot(object):
   

    def getKind(self):
        return 1

    def getName(self):
        return "人工智能V1号"

    def getPos(self,boardlist):
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
            player_number = 2
            enemy_number = 1
        else : #该黑棋下
            player_number = 1
            enemy_number = 2

        mx=my=ex=ey=max_score=my_max_score=enemy_max_score=-1    
        
        for i in range(row):
            for j in range(column):
                if boardlist[i][j]!=1 and boardlist[i][j]!=2:
                
                    my_score=oneScore(boardlist,player_number,i,j)   # 我方分数
                    enemy_score=oneScore(boardlist,enemy_number,i,j) # 敌方分数

                    if my_score > my_max_score :
                        my_max_score = my_score
                        mx = j
                        my = i
                    if enemy_score > enemy_max_score :
                        enemy_max_score = enemy_score
                        ex = j
                        ey = i
        
        if my_max_score>=enemy_max_score:
            max_score=my_max_score
            x=mx
            y=my
        else :
            max_score=enemy_max_score
            x=ex
            y=ey
        return (x,y,max_score)
    
'''智能机器  类定义结束'''


def getScore(s):  #对具体某个方向的打分
    
    base = [0,1,2,3,4,5] #棋子个数基数
    rank = 10  # 棋子个数幂底数

    if '11111' in s :   #五连
        return rank**base[5]*2   
    elif '011110' in s : #左右四
        return rank**base[4]*2  
    elif '0011100' in s : #左右三
        return rank**base[3]*2  
    elif '00011000' in s: #左右二
        return rank**base[2]*2  
    elif '000010000' in s: #左右一
        return rank**base[1]*2  
    elif '01111' in s or '11110' in s : # 单四
        return rank**base[4]
    elif '00111' in s or '11100' in s : # 单三
        return rank**base[3]
    elif '00011' in s or '11000' in s : # 单二
        return rank**base[2]
    elif '00001' in s or '10000' in s : # 单一
        return rank**base[1]
    else :
        return 0



#判断在某一点的八个方向分数总和
def oneScore(boardlist,player,i,j):
    score=0
    fake=copy.deepcopy(boardlist) #复制棋盘
    fake[i][j]=player #模拟在该位置落子

    row = column = len(boardlist)
    
    #限定这次落子可能影响的范围
    #上下左右 四正
    up=max(i-5,0)
    down=min(i+5,row-1)
    left=max(j-5,0)
    right=min(j+5,column-1)
    #四斜方向
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
    u_d=doCheck(u_d,player)
    l_r=doCheck(l_r,player)
    lu_rd=doCheck(lu_rd,player)
    ru_ld=doCheck(ru_ld,player)

    #计算总分数
    for s in (u_d,l_r,lu_rd,ru_ld):
        score+=getScore(s)
    return score


#校验传入的字符串，等于当前颜色的数字转化为1,不等于的转化为2，其他转化为0
def doCheck(s,player):
    result=''
    for x in s:
        if x=='1' or x=='2':
            if x==str(player):
                result+='1'    #自己方子
            else:
                result+='2'    #敌方子或者墙壁
        else:
            result+='0'        #空位
    return result

