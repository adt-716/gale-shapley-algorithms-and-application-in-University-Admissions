import pandas as pd
def stable_matching(majors, students, preferences, quotas):
    # Khởi tạo các cặp ghép nối rỗng cho mỗi ngành và sinh viên
    matches = {m: [] for m in majors}  # Ghép nối cho ngành
    student_matches = {s: None for s in students}  # Ghép nối cho sinh viên

    # Lặp khi còn sinh viên chưa được ghép nối và còn nguyện vọng
    while any(preferences[s] for s in students if student_matches[s] is None):
        for s in students:
            # Nếu sinh viên chưa có ghép nối và còn nguyện vọng
            if student_matches[s] is None and preferences[s]:
                m = preferences[s].pop(0)  # Ngành đầu tiên trong danh sách nguyện vọng của sinh viên
                # Nếu ngành này chưa đủ chỉ tiêu
                if len(matches[m]) < quotas[m]:
                    matches[m].append(s)
                    student_matches[s] = m
                else:
                    # Nếu ngành đã đủ chỉ tiêu, so sánh và thay thế nếu cần
                    try:
                        least_preferred = min(matches[m], key=lambda x: majors[m].index(x))
                        if majors[m].index(s) < majors[m].index(least_preferred):
                            # Thay thế sinh viên kém nhất bằng sinh viên hiện tại
                            matches[m].remove(least_preferred)
                            student_matches[least_preferred] = None
                            matches[m].append(s)
                            student_matches[s] = m
                        else:
                            # Ngành m giữ số lượng sinh viên đã có, không có thay đổi
                            pass  # Sinh viên s sẽ tiếp tục tìm kiếm ngành tiếp theo trong danh sách nguyện vọng
                    except ValueError:
                        print(f"Sinh viên {s} không có trong danh sách ưu tiên của ngành {m}")

    # Kiểm tra và thông báo sinh viên không đỗ ngành nào
    students_not_matched = [s for s in students if student_matches[s] is None and not preferences[s]]
    if students_not_matched:
        print("Sinh viên sau đây không đỗ vào ngành nào:")
        for s in students_not_matched:
            print(s)
    
    return matches, students_not_matched
def read_output_files(output1_path, output2_path):
    # Đọc dữ liệu từ file output1.txt
    with open(output1_path, 'r', encoding='utf-8') as f1:
        lines1 = f1.readlines()
    
    # Đọc dữ liệu từ file output2.txt
    with open(output2_path, 'r', encoding='utf-8') as f2:
        lines2 = f2.readlines()

    # Khởi tạo danh sách các sinh viên và nguyện vọng của họ
    students = []
    preferences = {}
    quotas = {}
    majors = {}

    # Parse output1.txt
    for line in lines1:
        line = line.strip()
        if line:
            parts = line.split(":")
            cccd = parts[0].strip()
            ma_nganh_list = parts[1].strip().split(", ")
            students.append(cccd)
            preferences[cccd] = ma_nganh_list

    # Parse output2.txt
    for line in lines2:
        line = line.strip()
        if line:
            parts = line.split(":")
            ma_nganh = parts[0].strip()
            ten_list = parts[1].strip().split(", ")
            majors[ma_nganh] = ten_list
            quotas[ma_nganh] = len(ten_list)  # Số sinh viên trong danh sách là chỉ tiêu của ngành học

    return majors, students, preferences, quotas



# Đọc dữ liệu từ các file output1.txt và output2.txt
majors, students, preferences, quotas = read_output_files('output1.txt', 'output2.txt')

# Thực hiện thuật toán ghép cặp ổn định
matches, students_not_matched = stable_matching(majors, students, preferences, quotas)

# Tạo danh sách sinh viên đỗ ngành
matched_data = []
for m, s_list in matches.items():
    for s in s_list:
        matched_data.append([s, m])

# Tạo DataFrame cho sinh viên đỗ ngành
df_matched = pd.DataFrame(matched_data, columns=['CCCD', 'Mã ngành'])

# Tạo DataFrame cho sinh viên không đỗ ngành
df_not_matched = pd.DataFrame(students_not_matched, columns=['CCCD'])
df_not_matched['Mã ngành'] = None

# Ghi kết quả vào file Excel
with pd.ExcelWriter('result.xlsx') as writer:
    df_matched.to_excel(writer, sheet_name='Sinh viên đỗ', index=False)
    df_not_matched.to_excel(writer, sheet_name='Sinh viên không đỗ', index=False)

print("Kết quả đã được ghi vào file result.xlsx")
