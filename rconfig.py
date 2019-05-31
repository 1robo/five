#每个下棋机器人文件代表一种新的下棋策略
# 先import 导入再定义 robots_file 元组内容
# 注意robot类中getKind的值要和元组位置对应

import human
import ai_1
import ai_2
import ai_3

#robot类getKind值  0      1      2      3 
robots_file =  ("human","ai_1","ai_2","ai_3")

robots_name=[]

for item in robots_file :
        robots_name.append(eval(item).robot().getName())

#获取robot类
def getRobot(tmp):
        for i in range(len(robots_name)):
                if tmp==robots_name[i]:
                        return eval(robots_file[i]).robot()
                
#棋盘配置
        
#长和宽
row=19    
column=19

#每步棋延时毫秒
delay = 300 






