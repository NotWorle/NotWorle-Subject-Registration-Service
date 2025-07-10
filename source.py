import tkinter.messagebox
import requests
import json
import  inspect
import time
import threading


class HocPhanUTH:
    CLC = '0104'
    DAITRA = '0101'
    TIENTIEN = '0120'
    def __init__(self, token:str):
        self.token = token
        self.base_url = 'https://portal.ut.edu.vn/api/v1/dkhp'
        self.headers = {
            'authorization': f'Bearer {token}',
            'content-type': 'application/json',
        }

    @staticmethod
    def read_json(namefile:str):
        with open(namefile, 'r', encoding='utf-8') as f:
            return json.load(f)


    @staticmethod
    def save_to_json(data, filename:str):
        caller_name = inspect.stack()[1].function

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"✅{caller_name} dữ liệu vào file '{filename}'")



    def is_class_full(self, code_subject, semester, code_class: str)->bool:
        self.get_subject(code_subject, semester)
        data = self.read_json('classIn4.json')

        for clas in data['body']:
            if clas['maLopHocPhan'] == code_class and clas['phanTramDangKy'] == 100:
                return True
        return False

    '''Get a list of subject code'''
    def get_subject(self, code_subject, semester:int, is_loc_trung:bool=False, is_loc_trong_0learning:bool=False):
        response = requests.get(
            f'{self.base_url}/getLopHocPhanChoDangKy',
            headers=self.headers,
            params={
                'idDot': semester,
                'maHocPhan': code_subject,
                'isLocTrung': is_loc_trung,
                'isLocTrungWithoutElearning': is_loc_trong_0learning,
            }
        )
        data = response.json()
        self.save_to_json(data,"classIn4.json")

    '''Get a list of subjects code'''
    def list_subject(self, code_subject:list, semester:int, is_loc_trung:bool=False, is_loc_trong_0learning:bool=False):
        data = []
        for code in code_subject:
            self.get_subject(f'0104{code}', semester, is_loc_trung, is_loc_trong_0learning)
            classes = self.read_json('classIn4.json')
            data.append(classes)
        
        self.save_to_json(data, 'classIn4.json')
        
        
            

    def get_subject_detail(self,id_class):
        response = requests.get(
            f'{self.base_url}/getLopHocPhanDetail',
            headers=self.headers,
            params={
                'idLopHocPhan': id_class,
            }
        )
        data = response.json()
        self.save_to_json(data,"classDetail.json")

    def register_subject(self,id_class):
        response = requests.post(
            f'{self.base_url}/dangKyLopHocPhan',
            headers=self.headers,
            params = {
                'idLopHocPhan': id_class,
            }
        )
        data = response.json()
        self.save_to_json(data,'ResponseRegister.json')


    def registered_list(self, semester:int):
        response = requests.get(
            f'{self.base_url}/getLHPDaDangKy',
            headers=self.headers,
            params = {
                'idDot': semester,
            }
        )
        data = response.json()
        self.save_to_json(data,'RegisteredList.json')

    def cancel_class(self, id_registered):
        response = requests.delete(
            f'{self.base_url}/huyDangKy',
            headers=self.headers,
            params = {
                'idDangKy': id_registered,
            }
        )
        data = response.json()
        self.save_to_json(data,'ResponseCancel.json')

    def auto_register(self, id_subject, latency:float=5, limit=None):
        if latency <= 0:
            print("Latency must be greater than 0")
            return False
        count = 0
        limit = 1200
        while True:
            if count > limit:
                print("Timeout for tool, registration failed")
                return False
            self.register_subject(id_subject)
            time.sleep(latency)
            response = self.read_json('ResponseRegister.json')
            if response['message'] != 'Lớp học phần đã đủ số lượng':
                print("Congratulations, registration successful")
                return True
            print(f' {count}')
            count += 1

    '''
    [
        {
            'id'=1,
            'maLopHocPhan'='13'
            'date'=[
                {
                    'thu':3
                }
            ]
        },
        
        {
            'id'=2,
            'maLopHocPhan'='43'
            'date'=[
                {
                    'thu':3
                },
                {
                    'thu':4
                }
            ]
        }
    ]
    '''
    def get_calendar(self, code_subject, semester:int):
        self.get_subject(code_subject, semester)
        classes = self.read_json('classIn4.json')
        date = [
            {'id':date['id'],
             'maLopHocPhan':date['maLopHocPhan'],
             'tenMonHoc':date['tenMonHoc'],
             'phanTramDangKy':date['phanTramDangKy']}
            for date in classes['body']
        ]

        for i in range(0,len(date)):
            self.get_subject_detail(date[i]['id'])
            day = self.read_json('classDetail.json')
            date[i]['date'] = day['body']

        with open('calendar.json','w', encoding='utf-8') as f:
            json.dump(date, f, ensure_ascii=False, indent=4)
        print('Generated calendar in calendar.json')


import tkinter as tk



subjects = ['127000', '122101', '127105', '127108', '123039', '127106', '127109', '127111', '127113']
LeDucHuy = HocPhanUTH('eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIwNzUyMDUwMDk2OTMiLCJpYXQiOjE3NTE4OTY3MTQsImV4cCI6MTc1NDQ4ODcxNH0.-Gq_Zy6CZjQ_RRE4idVNpO4aYx_iiDRWG5vaTM8KQvo')

LeDucHuy.get_subject(f'{LeDucHuy.CLC}122101', 73)

LeDucHuy.register_subject('141524')
code = ['010408010303', '010408010301', '012008010342']

# found = True
# while found:
#     for i in code:
#         if LeDucHuy.is_class_full(f'{LeDucHuy.CLC}080103', 73,i):
#             print(f"{i} FULL me roi")
#         else:
#             time.sleep(5)
#             root = tk.Tk()
#             root.withdraw()
#             root.attributes('-topmost', True)  # 👉 Ép cửa sổ lên trên cùng
#             tkinter.messagebox.showinfo("Đăng ký", "Có thằng óc chó hủy lớp rồi kìa")
#             root.destroy()  # Đóng cửa sổ gốc
#             found = False
#             break
#         time.sleep(1)
#     time.sleep(5)


# data = LeDucHuy.read_json('temp.json')
# ai = [[] for i in range(0,8)]
# logic = [[] for i in range(0,8)]

# for da in data:
#     # if da['phanTramDangKy'] == 100:
#     #     continue
#     what = {
#         'Trí tuệ nhân tạo và ứng dụng': ai,
#         'Tư duy thiết kế và đổi mới sáng tạo': logic,
#         'Đổi mới sáng tạo và Tư duy thiết kế': logic
#     }
#     print(f'{da['maLopHocPhan']}, {da['tenMonHoc']}, {da['phanTramDangKy']}')
#     for day in da['date']:
#         begin = day['ngayBatDau'][:11].split('-')
#         end = day['ngayKetThuc'][:11].split('-')
#         if int(end[1]) - int(begin[1]) >=1:
#             what[da['tenMonHoc']][day['thu']].append(da['maLopHocPhan'])
#             print(day)
#     print()

# for day in range(0,8):
#     print(f'thu {day}:\nAI: {ai[day]}\nLogic:{logic[day]}')

# LeDucHuy.get_calendar('0104080104', 73)
# time.sleep(10)
# LeDucHuy.get_calendar('0104080103', 73)



# 'C:\Users\Huy Le\Desktop\Programming language\Python\SelenimumTest\UTH'

'''
thu 3:
'''