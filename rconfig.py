import human
import ai_1
import ai_2
import ai_3





robots_name = ("=普通人类=","人工智能V1号","人工智能V2号","人工智能V3号")
robots_file = ("human","ai_1","ai_2","ai_3")

row=19    #棋盘大小
column=19

def getRobot(tmp):
        for i in range(len(robots_name)):
                if tmp==robots_name[i]:
                        return eval(robots_file[i]).robot()



