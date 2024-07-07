import pandas as pd

# Hàm đọc điểm số từ file
def read_scores(file_path):
    scores = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(': ', 1)
                if len(parts) != 2:
                    continue
                student = parts[0]
                scores[student] = {}
                subjects_scores = parts[1].split(', ')
                for subject_score in subjects_scores:
                    if ': ' in subject_score:
                        subject, score = subject_score.split(': ')
                        scores[student][subject] = float(score)
    return scores

# Hàm đọc sở thích của sinh viên từ file
def read_student_preferences(file_path):
    student_preferences = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(': ', 1)
                if len(parts) != 2:
                    continue
                student = parts[0]
                preferences = parts[1].split(', ')
                student_preferences[student] = preferences
    return student_preferences

# Hàm đọc thông tin về số lượng sinh viên tối đa của các trường từ file
def read_university_capacities(file_path):
    university_capacities = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(': ')
                if len(parts) != 2:
                    continue
                university, capacity = parts
                university_capacities[university] = int(capacity)
    return university_capacities

# Đọc dữ liệu từ các file
scores_file = 'output3.txt'
student_preferences_file = 'output1.txt'
university_capacities_file = 'output2.txt'

scores = read_scores(scores_file)
student_preferences = read_student_preferences(student_preferences_file)
university_capacities = read_university_capacities(university_capacities_file)

# Tạo danh sách sinh viên từ các key của student_preferences
students = list(student_preferences.keys())

# Hàm tính kết quả ghép đôi ổn định với điểm số
def stable_matching_with_scores(students, scores, university_capacities, student_preferences):
    matches = {u: [] for u in university_capacities}
    # Tạo một từ điển để theo dõi thứ tự nguyện vọng của mỗi sinh viên
    preference_order = {s: {u: i for i, u in enumerate(preferences)} for s, preferences in student_preferences.items()}
    
    # Sắp xếp sinh viên theo điểm số cao nhất của họ
    free_students = sorted(students, key=lambda x: max(scores[x].values()), reverse=True)
    rejected_students = []

    while free_students:
        s = free_students.pop(0)
        max_score = max(scores[s].values())
        preferred_universities = student_preferences.get(s, [])
        
        for u in preferred_universities:
            if u not in university_capacities:
                continue
            
            if len(matches[u]) < university_capacities[u]:
                matches[u].append(s)
                break
            else:
                current_students = matches[u]
                # Tìm sinh viên có điểm thấp nhất và nếu điểm bằng nhau, ưu tiên nguyện vọng
                worst_student = min(current_students, key=lambda x: (max(scores[x].values()), preference_order[x][u]))
                
                if (max_score > max(scores[worst_student].values()) or 
                   (max_score == max(scores[worst_student].values()) and preference_order[s][u] < preference_order[worst_student][u])):
                    matches[u].remove(worst_student)
                    matches[u].append(s)
                    free_students.append(worst_student)
                    # Cập nhật lại danh sách sinh viên tự do, sắp xếp theo điểm số cao nhất
                    free_students.sort(key=lambda x: max(scores[x].values()), reverse=True)
                    break
        else:
            rejected_students.append(s)  # No match found, add to rejected list

    return matches, rejected_students



# Thực hiện ghép đôi ổn định với điểm số từ dữ liệu đã nhập
matches, rejected_students = stable_matching_with_scores(students, scores, university_capacities, student_preferences)

# Tạo danh sách kết quả ghép đôi thành DataFrame
matches_list = [(u, student) for u, s in matches.items() for student in s]
matches_df = pd.DataFrame(matches_list, columns=['University', 'Student'])

# Tạo DataFrame danh sách sinh viên bị từ chối
rejected_students_df = pd.DataFrame(rejected_students, columns=['Rejected Students'])

min_scores = {}
for university, matched_students in matches.items():
    if matched_students:
        min_scores[university] = min(max(scores[student].values()) for student in matched_students)
    else:
        min_scores[university] = None
# Tạo DataFrame từ thông tin điểm chuẩn
min_scores_df = pd.DataFrame(min_scores.items(), columns=['University', 'Minimum Score'])

# Ghi dữ liệu vào file Excel
with pd.ExcelWriter('matching_results.xlsx') as writer:
    matches_df.to_excel(writer, sheet_name='Matches', index=False)
    rejected_students_df.to_excel(writer, sheet_name='Rejected Students', index=False)
    min_scores_df.to_excel(writer, sheet_name='Minimum Scores', index=False)

print("Kết quả ghép đôi ổn định và điểm chuẩn đã được ghi vào tệp 'matching_results.xlsx'.")