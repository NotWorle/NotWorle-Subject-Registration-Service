# Support University of Transport students in faster subject registration.

## Cách hoạt động
Dùng token của tài khoản sinh viên để gọi đến endpoint API
hệ thống của trường để thực hiên các chức năng liên quan đến học phần

## Các chức năng    
1. Lấy danh sách lớp theo mã học phần `class_list`:  
Trong đó:
   - `dao_tao:str`: mã ngành đào tạo
   - `subject_code:list`: mã học phần
   - `semester:int`: đợt đăng ký
   - `filename:str= r"data\class.json"`: nơi chứa danh sách lớp
   - `is_loc_trung:bool=False`: loại bỏ lớp đã đăng ký
   - `is_loc_trong_0learning:bool=False`:  không rõ  
Trả về `Tuple` response và danh sách `id_class`   

    ```
   Ví dụ:
    UTH = HocPhanUTH('I6MTc1NDgxNTE0N30.6adESgCAW8a1q9Hwv7tD51baqWzbhvqtKQPMEGMsaN0')
    subject_code = ['123013', '122041']
   
    id_class = LeDucHuy.class_list('0104', subject_code, 73)
   
    print(id_class['id'])
    print(id_class['data'])
    ```  


2. Xem lịch học của lớp `class_calendar`:  
Trong đó:
   - `id_class:list`: id của lớp
   - `filename:str= "data/calendar_class.json"`: nơi chứa danh sách
lịch học của lớp   
Trả về response
   
    ```
   # biến id_class['id'] ở ví dụ trên
   LeDucHuy.class_calendar(id_class['id'])
   ```


3. Đăng ký môn học `register_subject`:  
Trong đó:  
   - `id_class`: id của lớp   
Trả về response
   

4. Các môn học điều kiện đã đăng ký `registered_condition_subject`:  
    Trong đó:
   - `semester:int`: đợt đăng ký  
Trả về response và danh sách `id_registered`
   

5. Các môn học đã đăng ký `registered_subject`:  
    Trong đó:
   - `semester:int`: đợt đăng ký  
Trả về response và danh sách `id_registered`


6. Hủy đăng ký `cancel_class`:  
Trong đó:
   - `id_registered`: id môn học đã đăng ký
    Trả về response


7. Tự động đăng ký môn `auto_register`:
Trong đó:
    - `id_subject`: id lớp
    -  `latency:float=5`: độ trễ (5s)
    - `limit=2000`: giới hạn 2000 lần gửi request   


8. Xem tên giảng viên `name_teacher`:  
    Lưu ý:   Cần dùng token của một sinh viên khác để xem. 
    Lý do khi không có quyền truy cập khóa học nên bị đẩy trước cửa
    lớp nên mới thấy tên của giảng viên.

   Trong đó:
   - `semester:int`: đợt đăng ký
   - `class_code:list`: mã lớp học phần
   - `another_token:str`: token của sinh viên khác
    
   