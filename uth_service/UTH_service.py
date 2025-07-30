import requests
import json, time


class HocPhanUTH:
    """
    Thư viện hỗ trợ đăng ký lớp học phần tự động cho sinh viên trường UTH.
    """
    CLC = '0104'
    DAITRA = '0101'
    TIENTIEN = '0120'

    def __init__(self, token:str):
        self.token = token
        self.base_url = 'https://portal.ut.edu.vn/api/v1'
        self.course_url = 'https://courses.ut.edu.vn/course'
        self.headers = {
            'authorization': f'Bearer {token}',
            'content-type': 'application/json',
        }

    def is_class_full(self, dao_tao:str, subject_code, semester, class_code:str)->bool:
        self.get_class(dao_tao, subject_code, semester, class_code)
        data = self.read_json(r'data\class.json')

        for clas in data['body']:
            if clas['maLopHocPhan'] == class_code and clas['phanTramDangKy'] == 100:
                return True
        return False

    def semester(self, semester) -> dict:
        """
        Lấy danh sách các môn học theo đợt đăng ký.

        Parameters
        ----------
        semester : int
            Mã đợt đăng ký học phần.

        Returns
        -------
        response.json(): list
            Danh sách các môn học theo đợt đăng ký.
        """

        response = requests.get(
            f'{self.base_url}/dkhp/getHocPhanHocMoi',
            headers=self.headers,
            params={
                'idDot': semester,
            }
        )
        return response.json()

    def get_class(self,
                dao_tao:str,
                subject_code:str,
                semester:int,
                is_loc_trung:bool=False,
                is_loc_trong_0learning:bool=False):
        if not isinstance(subject_code, str) or not subject_code.isdigit() or len(subject_code) != 6:
            raise ValueError(f"Mã học phần không hợp lệ: {subject_code}")

        data = []

        urls = (
            [f'{self.base_url}/dkhpdk/getLopHocPhan', f'{self.base_url}/dkhp/getLopHocPhanChoDangKy']
            if dao_tao == ''
            else [f'{self.base_url}/dkhp/getLopHocPhanChoDangKy']
        )
      
        for u in urls:
            response = requests.get(
                u,
                headers=self.headers,
                params={
                    'idDot': semester,
                    'maHocPhan': f'{dao_tao}{subject_code}',
                    'isLocTrung': is_loc_trung,
                    'isLocTrungWithoutElearning': is_loc_trong_0learning,
                }
            )
            data.append(response.json())
        return data

    def get_id_class(self, class_code:str, semester:int):
        dao_tao = class_code[:4] if len(class_code) >= 12 else ''
        subject_code = class_code[4:10] if len(class_code) >= 12 else class_code[:6]
        
        data = self.get_class(dao_tao, subject_code, semester)
        for clas in data:
            for i in clas['body']:
                if i['maLopHocPhan'] == class_code:
                    return i['id']
        raise ValueError(f'Không tìm thấy lớp học phần với mã {class_code} trong đợt {semester}')

    def class_calendar(self, id_class:str):
        response = requests.get(
            f'{self.base_url}/dkhp/getLopHocPhanDetail',
            headers=self.headers,
            params={
                'idLopHocPhan': id_class,
            }
        )
        return response.json()

    def register_subject(self, id_class):
        response = requests.post(
            f'{self.base_url}/dkhp/dangKyLopHocPhan',
            headers=self.headers,
            params = {
                'idLopHocPhan': id_class,
            }
        )
        return response.json()


    def registered_condition_subject(self, semester:int):
        response = requests.get(
            f'{self.base_url}/dkhpdk/getLHPDaDangKy',
            headers=self.headers,
            params={
                'idDot': semester,
            }
        )
        return response.json()

    def registered_subject(self, semester:int):
        response = requests.get(
            f'{self.base_url}/dkhp/getLHPDaDangKy',
            headers=self.headers,
            params = {
                'idDot': semester,
            }
        )
        return response.json()
       

    def cancel_class(self, id_registered):
        response = requests.delete(
            f'{self.base_url}/dkhp/huyDangKy',
            headers=self.headers,
            params = {
                'idDangKy': id_registered,
            }
        )
        return response.json()

    def auto_register(self, id_class, latency:float=5, limit:int=2000):
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

    @staticmethod
    def solve_calendar(data):
        """
        Chuyển đổi dữ liệu lịch học thành định dạng dễ đọc.
        """

        for day in data:
            print(f'''Thứ: {day['thu']}
Tiết: {day['tietHoc']}
Phòng: {day['phong']}
{day['ngayBatDau'][:10]} đến {day['ngayKetThuc'][:10]} 
                    ''')
    
    def calander_simply(self, class_code:str, semester:str):
        """
        Lấy lịch học của lớp học phần theo mã lớp học phần và đợt đăng ký.
        """
        id_class = self.get_id_class(class_code, semester)
        data = self.class_calendar(id_class)
        self.solve_calendar(data['body'])
