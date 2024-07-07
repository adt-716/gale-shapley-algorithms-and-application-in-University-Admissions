import pandas as pd
from pandasql import sqldf

# Đọc dữ liệu từ các sheet trong file Excel
df_nguyen_vong = pd.read_excel('du_lieu.xlsx', sheet_name='Nguyện vọng')
df_diem_xet = pd.read_excel('diem_xet.xlsx')
df_thong_tin_sinh_vien = pd.read_excel('du_lieu.xlsx', sheet_name='Thông tin thí sinh')

# Kiểm tra tên các cột trong mỗi DataFrame
print("Nguyện vọng columns:", df_nguyen_vong.columns)
print("Điểm xét columns:", df_diem_xet.columns)
print("Thông tin thí sinh columns:", df_thong_tin_sinh_vien.columns)

# Định nghĩa câu truy vấn SQL
query = '''
        SELECT nv."Mã ngành", ts."Tên", dx."Diem xet THPT"
        FROM df_nguyen_vong nv
        JOIN df_thong_tin_sinh_vien ts ON nv.CCCD = ts.CCCD
        JOIN df_diem_xet dx ON nv.CCCD = dx.CCCD
        '''

# Thực thi câu truy vấn SQL
result = sqldf(query, locals())

# Kiểm tra kết quả truy vấn
print("Kết quả truy vấn:")
print(result.head())

# Sắp xếp dữ liệu dựa trên cột 'Mã ngành' và 'Điểm xét Max' giảm dần
sorted_df = result.sort_values(by=['Mã ngành', 'Diem xet THPT'], ascending=[True, False])

# Tạo danh sách chứa các dòng kết quả theo yêu cầu
lines = []
for ma_nganh, group in sorted_df.groupby('Mã ngành'):
    ten = ', '.join(group['Tên'].astype(str))
    lines.append(f"{ma_nganh}: {ten}")

# Ghi danh sách dòng dữ liệu vào file văn bản
with open('output2.txt', 'w', encoding='utf-8') as f:
    for line in lines:
        f.write(line + '\n')

print("Dữ liệu đã được ghi vào file output2.txt")
