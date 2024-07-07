import pandas as pd
from pandasql import sqldf

# Đọc dữ liệu từ các sheet trong file Excel

df_diem_xet = pd.read_excel('diem_xet.xlsx')
df_thong_tin_sinh_vien = pd.read_excel('du_lieu.xlsx', sheet_name='Thông tin thí sinh')

# Kiểm tra tên các cột trong mỗi DataFrame

print("Điểm xét columns:", df_diem_xet.columns)
print("Thông tin thí sinh columns:", df_thong_tin_sinh_vien.columns)

# Định nghĩa câu truy vấn SQL
query = '''
        SELECT ts."Tên", ts."CCCD", dx."Diem xet THPT", dx."Mã ngành"
        from df_thong_tin_sinh_vien ts
        JOIN df_diem_xet dx ON ts.CCCD = dx.CCCD
        '''

# Thực thi câu truy vấn SQL
result = sqldf(query, locals())

# Kiểm tra kết quả truy vấn
print("Kết quả truy vấn:")
print(result.head())


sorted_df = result.sort_values(by=['CCCD', 'Diem xet THPT'], ascending=[True, False])

# Tạo danh sách chứa các dòng kết quả theo yêu cầu
lines = []
for cccd, group in sorted_df.groupby('CCCD'):
        details = [f"{row['Mã ngành']}: {row['Diem xet THPT']}" for index, row in group.iterrows()]
        details_str = ', '.join(details)
        lines.append(f"{cccd}: {details_str}")


# Ghi danh sách dòng dữ liệu vào file văn bản
with open('output3.txt', 'w', encoding='utf-8') as f:
    for line in lines:
        f.write(line + '\n')

print("Dữ liệu đã được ghi vào file output3.txt")
