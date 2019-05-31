#下棋机器人培训文件
#所有新建的下棋策略
# 先import 导入
#再加上名称和文件名

import human
import ai_1
import ai_2
import ai_3





robots_file=("human","ai_1","ai_2","ai_3")

robots_name=[]

for item in robots_file :
        robots_name.append(eval(item).robot().getName())
        
#棋盘大小
row=19    
column=19

#获取robot类
def getRobot(tmp):
        for i in range(len(robots_name)):
                if tmp==robots_name[i]:
                        return eval(robots_file[i]).robot()




