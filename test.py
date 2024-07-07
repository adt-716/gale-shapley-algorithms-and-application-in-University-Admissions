import pandas as pd
from pandasql import sqldf
# Đọc dữ liệu từ sheet cụ thể trong file Excel
df_nguyen_vong = pd.read_excel('du_lieu.xlsx', sheet_name='Nguyện vọng')
df_thong_tin_thi_sinh = pd.read_excel('du_lieu.xlsx', sheet_name='Thông tin thí sinh')
query = '''
        SELECT *
        FROM df_nguyen_vong nv
        JOIN df_thong_tin_thi_sinh ts ON nv.CCCD = ts.CCCD

        '''

# Thực thi câu truy vấn SQL
result = sqldf(query, locals())
# Lọc các dòng trùng lặp
#duplicated_rows = result[result.duplicated(subset=['CCCD','Tên'], keep=False)]

# Sắp xếp dữ liệu dựa trên cột CCCD và thứ tự nguyện vọng
sorted_df = result.sort_values(by=['CCCD', 'Thứ tự nguyện vọng'])

# Tạo một danh sách các dòng dữ liệu
lines = []

# Thêm các dòng dữ liệu vào danh sách
for cccd, group in sorted_df.groupby('CCCD'):
    ma_nganh = ', '.join(group['Mã ngành'].astype(str) )
    lines.append(f"{cccd}: {ma_nganh}")

# Ghi danh sách dòng dữ liệu vào file văn bản
with open('output1.txt', 'w') as f:
    for line in lines:
        f.write(line + '\n')