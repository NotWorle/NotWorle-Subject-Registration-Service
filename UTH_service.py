import requests
import json
import  inspect
import time


class HocPhanUTH:
    CLC = '0104'
    DAITRA = '0101'
    TIENTIEN = '0120'

    CALENDAR = [
        [[]]
        for day in range(2,8)
    ]

    def __init__(self, token:str):
        self.token = token
        self.base_url = 'https://portal.ut.edu.vn/api/v1/dkhp'
        self.course_url = 'https://courses.ut.edu.vn/course'
        self.headers = {
            'authorization': f'Bearer {token}',
            'content-type': 'application/json',
        }

    # @staticmethod
    # def check_token(data):
    #     if data["message"] == "Invalid JWT token":
    #         raise Exception('Invalid JWT token')
    #     return True
    @staticmethod
    def validate_subject_codes(subject_code: list[str]):
        for code in subject_code:
            if not isinstance(code, str) or not code.isdigit() or len(code) != 6:
                raise ValueError(f"Mã học phần không hợp lệ: {code}")

    @staticmethod
    def read_json(namefile:str):
        with open(namefile, 'r', encoding='utf-8') as f:
            return json.load(f)


    @staticmethod
    def save_to_json(data, filename:str):
        caller_name = inspect.stack()[1].function

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"{caller_name} trả lời dữ liệu tại file '{filename}'")



    def is_class_full(self, dao_tao:str, subject_code, semester, class_code:str)->bool:
        self.class_list(dao_tao, subject_code, semester, class_code)
        data = self.read_json(r'data\class.json')

        for clas in data['body']:
            if clas['maLopHocPhan'] == class_code and clas['phanTramDangKy'] == 100:
                return True
        return False


    def class_list(self,
                   dao_tao:str,
                   subject_code:list,
                   semester:int,
                   filename:str= "data/class.json",
                   is_loc_trung:bool=False,
                   is_loc_trong_0learning:bool=False):
        self.validate_subject_codes(subject_code)

        data = []
        id_class = []
        for code in range(len(subject_code)):
            response = requests.get(
                f'{self.base_url}/getLopHocPhanChoDangKy',
                headers=self.headers,
                params={
                    'idDot': semester,
                    'maHocPhan': f'{dao_tao}{subject_code[code]}',
                    'isLocTrung': is_loc_trung,
                    'isLocTrungWithoutElearning': is_loc_trong_0learning,
                }
            )
            temp = response.json()
            data.append({
                'subjectCode': subject_code[code],
                'body': response.json(),
            }
            )
            for clas in temp['body']:
                id_class.append(clas['id'])

        self.save_to_json(data, filename)
        return {
            'data': data,
            'id': id_class,
        }


    def class_calendar(self, id_class:list, filename:str= "data/calendar_class.json"):
        data = []
        for idx in id_class:
            response = requests.get(
                f'{self.base_url}/getLopHocPhanDetail',
                headers=self.headers,
                params={
                    'idLopHocPhan': idx,
                }
            )
            temp = {
                'id': idx,
                'body': response.json()
            }
            data.append(temp)
        self.save_to_json(data, filename)
        return data

    def register_subject(self, id_class):
        response = requests.post(
            f'{self.base_url}/dangKyLopHocPhan',
            headers=self.headers,
            params = {
                'idLopHocPhan': id_class,
            }
        )
        data = response.json()
        self.save_to_json(data,"data/ResponseRegister.json")
        return data


    def registered_condition_subject(self, semester:int):
        id_registered = []
        response = requests.get(
            f'https://portal.ut.edu.vn/api/v1/dkhpdk/getLHPDaDangKy',
            headers=self.headers,
            params={
                'idDot': semester,
            }
        )

        for idx in response.json()['body']:
            id_registered.append(idx['id'])

        data = response.json()
        self.save_to_json(data, r"data\Registered_Condition.json")
        return {
            'data': data,
            'id': id_registered,
        }

    def registered_subject(self, semester:int):
        id_registered = []
        response = requests.get(
            f'{self.base_url}/getLHPDaDangKy',
            headers=self.headers,
            params = {
                'idDot': semester,
            }
        )

        for idx in response.json()['body']:
            id_registered.append(idx['id'])

        data = response.json()
        self.save_to_json(data, r'data/Registered_Subject.json')
        return {
            'data': data,
            'id': id_registered,
        }

    def cancel_class(self, id_registered):
        response = requests.delete(
            f'{self.base_url}/huyDangKy',
            headers=self.headers,
            params = {
                'idDangKy': id_registered,
            }
        )

        data = response.json()
        self.save_to_json(data, r'data/Response_Cancel.json')
        return data

    def auto_register(self, id_class, latency:float=5, limit=2000):
        if latency <= 0:
            print("Latency must be greater than 0")
            return False
        count = 0
        while True:
            if count > limit:
                print("Timeout for tool, registration failed")
                return False
            response = self.register_subject(id_class)
            time.sleep(latency)
            if response['message'] != 'Lớp học phần đã đủ số lượng':
                print("Congratulations, registration successful")
                return True
            print(f' {count}')
            count += 1


    def name_teacher(self, semester:int, class_code:list, another_token:str):
        data = []
        for class_code in class_code:
            response = requests.get(
                f'{self.course_url}/view.php',
                headers=self.headers,
                params={
                    'idnumber': f'{semester}{class_code}',
                    'token': another_token,
                }
            )
            data.append(response.url)
        print(data)
        return data


