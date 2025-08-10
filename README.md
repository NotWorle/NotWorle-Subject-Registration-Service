# Support University of Transport students in faster subject registration.

## Cách hoạt động
Dùng token của tài khoản sinh viên để gọi đến endpoint API
hệ thống của trường để thực hiên các chức năng liên quan đến học phần
Tutorial: [Lấy token thủ công](https://youtu.be/UnA8YOCFXx0)

## Quy trình của hệ thống đăng ký
Sinh viên mở đợt đăng ký **semester**.
![alt text](images/image.png)

Tại mỗi đợt đăng ký **semester**, chứa các thông tin lớp trong đợt đăng ký,
Dùng hàm `def semester(self, semester)`.
![alt text](images/image-1.png)

Khi ấn vào 1 môn tức là gửi `dao_tao` và `subject_code` sẽ trả thông tin `class_code` (mã lớp học phần) của các lớp tương ứng. Thông tin trả về chứa một `id_class`.
Dùng hàm `def get_class`.
![alt text](images/image-2.png)

Ấn vào lớp, gửi `id_class` để xem lịch học của `class_code` (mã lớp học phần).
Dùng hàm `def get_class`.
![alt text](images/image-3.png)

Để đăng ký, gửi `id_class`
Dùng hàm `def register_subject(self, id_class)`.
![alt text](images/image-4.png)

Để xem danh sách môn (điều kiện) đã đăng ký:
Dùng hàm `def registered_subject(self, semester:int)` or `registered_subject(self, semester:int)`.
![alt text](images/image-5.png)

## Các chức năng. 
1.  `def semester(self, semester) -> dict:`
**Chức năng**: Xem các môn đăng ký theo *đợt đăng ký*
Tham số:
      - `semester:int`: đợt đăng ký.
**Return**: Dữ liệu json danh sách môn đăng ký theo `semester`.

2. `def get_class(self,
                dao_tao:str,
                subject_code:str,
                semester:int,
                is_loc_trung:bool=False,
                is_loc_trong_0learning:bool=False):`  
**Chức năng**: Lấy danh sách lớp theo *mã học phần* 
Tham số:
   - `dao_tao:str`: mã ngành đào tạo
   - `subject_code:str`: mã học phần
   - `semester:int`: đợt đăng ký
   - `is_loc_trung:bool=False`: loại bỏ lớp đã đăng ký
   - `is_loc_trong_0learning:bool=False`:  không rõ  
**Return**: Danh sách thông tin của từng lớp (`id_class`,...)

3. `def get_id_class(self, class_code:str, semester:int):`
**Chức năng**: Lấy `id_class` theo *mã lớp học phần* 
Tham số:
   - `class_code:str`: Mã lớp học phần.
   - `semester:int`: Đợt đăng ký
**Return**: Trả `id_class` tương ứng với `subject_code`.

4. `def class_calendar(self, id_class:str)`:
**Chức năng**: Xem lịch học của *mã lớp học phần* theo id tương ứng
   - `id_class:str`: id của lớp
**Return**: Trả lịch học tương ứng với `id_class`.

5. `def register_subject(self, id_class)`:  
**Chức năng**: Đăng ký lớp với id của lớp
   - `id_class:str`: id của lớp
**Return**: Repsone của việc đăng ký
   

6. `def registered_subject(self, semester:int)`:  
**Chức năng**: Xem các *môn điều kiện* đã đăng ký trong đợt.
   - `semester:int`: đợt đăng ký
**Return**: Trả danh sách *lớp môn điều kiện* đã đăng ký, chứa `id_registered`
   

7. `registered_subject(self, semester:int)`:  
**Chức năng**: Xem các *môn* đã đăng ký trong đợt.
   - `semester:int`: đợt đăng ký
**Return**: Trả danh sách lớp môn đã đăng ký, chứa `id_registered`

8. `def cancel_class(self, id_registered)`:  
**Chức năng**: Hủy lớp đã đăng ký.
   - `semester:int`: đợt đăng ký
**Return**: Response về việc hủy đăng ký


9. `def auto_register(self, id_class, latency:float=5, limit:int=2000):`:
**Chức năng**: Tự động đăng ký môn học.
   - `id_class`: id của lớp học phần
   - `latency:float=5`: độ trễ, mặc định 5 giây
   - `limit:int=2000`: giới hạn số lần thực hiện đăng ký, mặc định 2000
**Return**: None


## Example
### Xem danh sách lớp học theo `subject_code`
Với các môn điều kiện sẽ không có tham số `dao_tao`
```
UTH = HocPhanUTH('eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIwNzUyMDUwMDk2OTMiLCJpYXQiOjE3NTM4NTk1OTksImV4cCI6MTc1NjQ1MTU5OX0.57uZ2Bzopy7zIN-wejnQapyBwYXehks6qvgQZ6cb3w4')

# Môn học điều kiện dao_tao để trống
english = UTH.get_class('', '006111', 73)

# Môn máy học
machine = UTH.get_class('0104', '122101', 73)

# định dạng dumps json sẽ dễ học hơn
print(json.dumps(english, indent=4, ensure_ascii=False))
print(json.dumps(machine = UTH.get_class('0104', '122101', 73)
, indent=4, ensure_ascii=False))
```


2. Một vài chức năng khác
```
UTH = HocPhanUTH('eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIwNzUyMDUwMDk2OTMiLCJpYXQiOjE3NTM4NTk1OTksImV4cCI6MTc1NjQ1MTU5OX0.57uZ2Bzopy7zIN-wejnQapyBwYXehks6qvgQZ6cb3w4')
# Xem danh sach lớp theo đợt đăng ký
subject_sesmester = UTH.semester(73)

# Xem danh sach lớp theo mã học phần
list_class = UTH.get_class('', '006111', 73)

# Lấy id_class theo mã lớp học phần
id_class = UTH.get_id_class('010408010101',73)

# Xem lịch học của lớp
calendar = UTH.class_calendar(id_class)

# Xuất data
print(json.dumps(list_class, indent=4, ensure_ascii=False))

print(id_class)

print(json.dumps(calendar, indent=4, ensure_ascii=False))
```


