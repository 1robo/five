'''
3号机器人

'''
import copy


'''智能机器  类定义开始'''
 
class robot(object):
   

    def getKind(self):
        return 3

    def getName(self):
        return "人工智能V3号"

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

        max_score=0
        x = -1
        y = -1
        
        for i in range(row):
            for j in range(column):
                if boardlist[i][j]!=1 and boardlist[i][j]!=2:
                    my_score=oneScore(boardlist,player_number,i,j)
                    enemy_score=oneScore(boardlist,enemy_number,i,j)
                    score=my_score*2.5+enemy_score
                    if score>=max_score:
                        max_score=score
                        x=j
                        y=i
        
        return (x,y,int(max_score))
    
'''智能机器  类定义结束'''


def getScore(str1):  #对具体某个方向的打分
    str2=str1[::-1]
    if '11111' in str1 or '11111' in str2:#五连
        return 1000
    elif '011110' in str1 or '011110' in str2:#活四
        return 100
    elif '011101' in str1 or '011101' in str2:#跳活四情形1
        return 16
    else:
        for x in ('011112','101112','110112','111012'):#冲四
            if x in str1 or x in str2:
                return 15
        if '011100' in str1 or '011100' in str2:#连活三
            return 15
        if '010110' in str1 or '010110' in str2:#跳活三
            return 10
        if '001112' in str1 or '001112' in str2:#眠三
            return 2
        for x in ('011000','001100'):#连活2
            if x in str1 or x in str2:
                return 2
        if '010100' in str1 or '010100' in str2:#跳活二
            return 1
        if '000112' in str1 or '000112' in str2:#眠二
            return 0.2
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
