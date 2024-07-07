import pandas as pd
 # Đọc dữ liệu từ các sheet trong file Excel
df_thong_tin_sinh_vien = pd.read_excel('du_lieu.xlsx', sheet_name='Chỉ tiêu')
    
    # Kiểm tra tên các cột trong DataFrame
print("Thông tin thí sinh columns:", df_thong_tin_sinh_vien.columns)

    # Kiểm tra sự tồn tại của các cột 'Mã ngành' và 'Chỉ tiêu'
required_columns = ['Mã ngành', 'Chỉ tiêu']
for col in required_columns:
    if col not in df_thong_tin_sinh_vien.columns:
        raise KeyError(f"Cột '{col}' không tồn tại trong DataFrame")

    # Tạo danh sách chứa các dòng kết quả theo yêu cầu
lines = []
for index, row in df_thong_tin_sinh_vien.iterrows():
    ma_nganh = row['Mã ngành']
    chi_tieu = row['Chỉ tiêu']
    lines.append(f"{ma_nganh}: {chi_tieu}")

    # Ghi danh sách dòng dữ liệu vào file văn bản
with open('output2.txt', 'w', encoding='utf-8') as f:
    for line in lines:
        f.write(line + '\n')

print("Dữ liệu đã được ghi vào file output2.txt")
