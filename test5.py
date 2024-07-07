import pandas as pd
from pandasql import sqldf

# Đọc dữ liệu từ sheet cụ thể trong file Excel
df_thong_tin_thi_sinh = pd.read_excel('diem_xet.xlsx', sheet_name='Sheet1')
df_do = pd.read_excel('matching_results.xlsx', sheet_name='Matches')

# Xóa các hàng bị trùng trong df_thong_tin_thi_sinh
df_thong_tin_thi_sinh = df_thong_tin_thi_sinh.drop_duplicates(subset=['CCCD'])

query = '''
        SELECT *
        FROM df_thong_tin_thi_sinh ts
        JOIN df_do do ON do.Student = ts.CCCD
        where do.university = "CH1" ;
        '''

# Thực thi câu truy vấn SQL
result = sqldf(query, locals())

# Ghi dữ liệu đã được truy vấn vào file output5.txt
result.to_csv('output5.txt', index=False, sep='\t')

print("Dữ liệu đã được ghi vào file output5.txt")
