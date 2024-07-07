import pandas as pd
from pandasql import sqldf
# Đọc dữ liệu từ sheet cụ thể trong file Excel
df_chi_tieu = pd.read_excel('du_lieu.xlsx', sheet_name='Chỉ tiêu')
df_diem_chuan = pd.read_excel('matching_results.xlsx', sheet_name='Minimum Scores')
query = '''
        SELECT ct."Mã ngành" as "Mã ngành", ct."Tên ngành" as "Tên ngành", ct."Mã ngành chuẩn" as "Mã ngành chuẩn",
        ct."Chỉ tiêu" as "Chỉ tiêu", dc."Minimum Score" as "Điểm chuẩn"
        FROM df_chi_tieu ct
        inner JOIN df_diem_chuan dc ON ct."Mã ngành" = dc.University
        ;
        '''

# Thực thi câu truy vấn SQL
result = sqldf(query, locals())
# Lưu kết quả vào file Excel
result.to_excel('chi_tieu.xlsx', index=False)
