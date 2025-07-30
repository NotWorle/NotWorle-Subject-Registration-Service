from uth_service.UTH_service import HocPhanUTH
import json, time


UTH = HocPhanUTH('eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIwNzUyMDUwMDk2OTMiLCJpYXQiOjE3NTM4NTk1OTksImV4cCI6MTc1NjQ1MTU5OX0.57uZ2Bzopy7zIN-wejnQapyBwYXehks6qvgQZ6cb3w4')

# Môn học điều kiện dao_tao để trống
english = UTH.get_class('', '006111', 73)

# Môn máy học
machine = UTH.get_class('0104', '122101', 73)

# định dạng dumps json sẽ dễ học hơn
print(json.dumps(english, indent=4, ensure_ascii=False))
print(json.dumps(machine = UTH.get_class('0104', '122101', 73)
, indent=4, ensure_ascii=False))
