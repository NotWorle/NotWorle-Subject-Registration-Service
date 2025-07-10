import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



LOGIN = 'https://portal.ut.edu.vn/'
DASHBOARD = 'https://portal.ut.edu.vn/dashboard'
REGISTER = 'https://portal.ut.edu.vn/coursesregistration'
ALERT = 'không thể đăng ký do trùng lịch'
web = webdriver.Edge()

def convert_classto_css(clas:str):
    clas = clas.replace(' ','.')
    return clas

def login(username, password):
    time.sleep(3)
    web.find_element(By.ID, ':r0:').send_keys(username)
    web.find_element(By.ID, ':r1:').send_keys(password)

'''Điền thong tin o day'''
web.get('https://portal.ut.edu.vn/coursesregistration')
login('', '')






subject = 'Thể dục thể hình nâng cao - Fitness 2'
code = 'Mã lớp học phần: 010400412605'
'''Điền thong tin o day'''
'''Hươớng dẫn:
1. điên thong tin de dang ky
2. sau khi no tu dien tai khoan va pass thi nhanh tay an dang nhap
3. chiêm ngưỡng auto đăng ký
4. dam bao khong bi trung lich
'''

time.sleep(5)



i = 0

while True:
    print(f'Lần {i}')

    # Chose học kì
    web.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[3]/div/div/div[1]/div/div[2]/div[1]/div/div').click()
    print("Chosed hoc ki")
    time.sleep(1)
    # Chose học kì phụ
    clas1 = convert_classto_css(
        'MuiButtonBase-root MuiMenuItem-root MuiMenuItem-gutters MuiMenuItem-root MuiMenuItem-gutters css-12u307e')
    web.find_element(By.CLASS_NAME, clas1).click()
    print("Chosed hoc ki phu")
    time.sleep(1)

    #Tìm môm học
    try:
        p = web.find_element(By.XPATH, f"//p[text()='{subject}']")
        print(f'Đã tìm thấy môn học: {p.text}')
        p.click()
    except NoSuchElementException:
        print(f"Không thấy tên môn học: {subject}")


    time.sleep(2)


    ps = web.find_elements(By.TAG_NAME, "p")
    search = False
    for p in ps:
        if code in p.text:
            print("Đã tìm thấy:", p.text)
            search = True
            p.click()
            break
    if not search:
        print(f'Không tìm thấy: {code}')

    time.sleep(2)

    #click register button
    try:
        register = web.find_element(By.XPATH,'//*[@id="root"]/div[1]/div[3]/div/div/div[3]/div/div[2]/div[2]/button')
        if register.get_attribute("disabled"):
            print("Nút đã bị vô hiệu hóa (disabled), không thể click")
        else:
            register.click()
            print("Dang ky thanh cong")
            break
    except NoSuchElementException:
        print("Full members")
    web.refresh()
    time.sleep(2)
    i+=1


web.quit()

