import pandas as pd
from pandasql import sqldf
# Đọc dữ liệu từ sheet cụ thể trong file Excel
df_diem_xet = pd.read_excel('diem_xet.xlsx', sheet_name='Sheet1')
df_thong_tin_thi_sinh = pd.read_excel('du_lieu.xlsx', sheet_name='Thông tin thí sinh')
df_thi_sinh_do = pd.read_excel('matching_results.xlsx', sheet_name='Matches')
query = '''
        SELECT dx.CCCD as CCCD, ts."Tên" as "Tên", dx."Mã ngành" as "Mã ngành", dx."Thứ tự nguyện vọng" as "Thứ tự nguyện vọng",
        dx."Diem xet THPT" as "Điểm xét THPT" 
        FROM df_diem_xet dx
        inner JOIN df_thong_tin_thi_sinh ts ON dx.CCCD = ts.CCCD
        inner Join df_thi_sinh_do do on dx.CCCD = do.Student 
        where dx."Mã ngành" = do.University
        GROUP BY do.Student ,do.University;
        '''

# Thực thi câu truy vấn SQL
result = sqldf(query, locals())
# Lưu kết quả vào file Excel
result.to_excel('ket_qua.xlsx', index=False)

