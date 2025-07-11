from UTH_service import HocPhanUTH

LeDucHuy = HocPhanUTH('eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIwNzUyMDUwMDk2OTMiLCJpYXQiOjE3NTIyMjMxNDcsImV4cCI6MTc1NDgxNTE0N30.6adESgCAW8a1q9Hwv7tD51baqWzbhvqtKQPMEGMsaN0')

subject_code = ['123013', '122041']

id_class = LeDucHuy.class_list('0104', subject_code, 73)

print(id_class['id'])
print(id_class['data'])
LeDucHuy.class_calendar(id_class['id'])


