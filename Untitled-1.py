import cv2
import numpy as np
import pyautogui
import pytesseract

import time
import re
from skimage.metrics import structural_similarity as ssim
pyautogui.PAUSE = 0.1

# 若要终止程序，可在识别失败5次时将鼠标移至角落

pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\Tesseract-OCR\tesseract.exe'

not_found_count = 0     #记录失败次数，若超过5次，则终止程序，可按需调整
succeed_count = 0       #记录成功次数，若超过10次，则本轮结束，可按需调整

def capture_area():
    region = (300, 322, 380, 150)  # (x, y, width, height) 坐标是由上到下，由左到右的;此坐标是识别区域坐标
    screenshot = pyautogui.screenshot(region=region)
    image=np.array(screenshot)
    return image

def preprocess_image(image):
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 应用高斯模糊
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # 自动阈值处理
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def recognize_numbers(image):
    
    thresh = preprocess_image(image)  # 对图像进行预处理
    text = pytesseract.image_to_string(thresh, config='--psm 6')
    numbers = [int(num) for num in re.findall(r'\d+', text)]
    return numbers

def draw_comparison(numbers):
    global not_found_count,succeed_count
    #识别失败的情况
    if len(numbers)!=2:
        print("The numbers is error!",numbers)
        not_found_count+=1

        if not_found_count>=5: #识别失败次数大于5，认为该轮游戏结束，进入下一轮
            time.sleep(2)
            pyautogui.click(490, 870) # 此坐标是“开心收下”按钮的坐标
            time.sleep(0.5)
            pyautogui.click(634, 1030) # 此坐标是“继续”按钮的坐标
            time.sleep(0.5)
            pyautogui.click(500,950) # 此坐标是“继续PK”按钮的坐标
            time.sleep(11)  #匹配等待时间
            
            print("准备重新开始程序...")
            # 一轮结束，清除标记
            not_found_count=0
            succeed_count=0
            time.sleep(1)
            main()

        #失败次数小于5，可能为图像识别错误，重新识别
        return
    
    # 识别成功的情况
    first, second = numbers[0], numbers[1]
    origin_x, origin_y = 480, 714  # 此坐标是绘制区域是坐标
    size = 50   #偏移量（绘画线段长度）

    if first > second:
        print(f"{first} > {second}")
        draw_greater_than(origin_x, origin_y, size)
    elif first < second:
        print(f"{first} < {second}")
        draw_less_than(origin_x, origin_y, size)
    # 功能拓展：两个数相等的情况
    # else:
        # draw_equal_than(origin_x,origin_y,size)

    # 由于识别成功，说明游戏没有结束，重新记录失败次数
    succeed_count += 1
    not_found_count = 0  
# 大于符号
def draw_greater_than(origin_x, origin_y, size):
    pyautogui.moveTo(origin_x, origin_y)
    pyautogui.dragRel(size, size, duration=0.01)
    pyautogui.dragRel(-size, size, duration=0.01)
# 小于符号
def draw_less_than(origin_x, origin_y, size):
    pyautogui.moveTo(origin_x + size, origin_y)
    pyautogui.dragRel(-size, size, duration=0.01)
    pyautogui.dragRel(size, size, duration=0.01)
#等于符号(拓展功能)
# def draw_equal_than(origin_x,origin_y,size):
#     pyautogui.moveTo(origin_x,origin_y)
#     pyautogui.dragRel(size,0,duration=0.05)
#     pyautogui.moveTo(origin_x+size,origin_y)
#     pyautogui.dragRel(size,0,duration=0.05)

# def has_image_changed(image1,image2):
#     # 使用结构相似度指数SSIM
#     # 将图像转换为灰度图像
#     gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY).astype(np.float64) / 255.0
#     gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY).astype(np.float64) / 255.0
#     # 确保图像至少为 7x7 像素
#     if gray_image1.shape[0] < 7 or gray_image1.shape[1] < 7 or gray_image2.shape[0] < 7 or gray_image2.shape[1] < 7:
#         return False  # 图像太小，无法计算 SSIM
#     # 计算两个图像的 SSIM
#     similarity = ssim(gray_image1, gray_image2,data_range=1.0)
    
#     return similarity < 0.9

def main():
    global not_found_count,succeed_count

    # previous_image = None
    # not_changed_count=0
    try:
        while not_found_count<5 and succeed_count<15:   #将循环成功次数设置偏大避免重复识别到同一组数据导致提前结束
            image = capture_area() #图像识别区域

            # if previous_image is not None and not_changed_count<3 and not has_image_changed(previous_image,image):
            #     print("图像未变化，跳过处理")
            #     not_changed_count+=1
            #     time.sleep(0.1)
            #     continue
            
            # previous_image=image
            # print("图片已经替换")
            # print(not_changed_count)

            numbers = recognize_numbers(image)
            draw_comparison(numbers)
            time.sleep(0.35) # 每次绘画及识别的延迟
    except SystemExit as e:
        print(e)

if __name__ == "__main__":
    main()
