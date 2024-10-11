import pyautogui as pg
import time
# pg.moveTo(292,322,duration=0.1)
# time.sleep(3)
# pg.dragTo(655,322,duration=1)
# pg.dragTo(655,450,duration=1)
# pg.dragTo(292,450,duration=1)
# pg.dragTo(292,322,duration=1)
# 292, 322, 655, 450
# 获取鼠标坐标值
time.sleep(3)
x,y=pg.position()
print(x,y)