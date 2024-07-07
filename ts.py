def stable_matching_with_scores(students, scores, university_capacities, student_preferences):
    # Khởi tạo tập hợp trống cho các trường đại học
    matches = {u: [] for u in university_capacities}
    free_students = sorted(students, key=lambda x: scores[x], reverse=True)  # Ưu tiên điểm cao hơn

    # Tạo danh sách các trường mà sinh viên có thể nộp đơn
    student_proposals = {s: list(prefs) for s, prefs in student_preferences.items()}
    
    # Danh sách các sinh viên không đỗ
    rejected_students = set(students)
    
    while free_students:
        s = free_students.pop(0)
        
        # Lấy trường mà sinh viên s thích nhất nhưng chưa nộp đơn
        if student_proposals[s]:
            u = student_proposals[s].pop(0)
        else:
            continue
        
        if len(matches[u]) < university_capacities[u]:
            # Trường còn chỉ tiêu
            matches[u].append(s)
            rejected_students.discard(s)  # Sinh viên đã được nhận
        else:
            # Trường đã đủ chỉ tiêu
            current_students = matches[u]
            # Tìm thí sinh có điểm thấp nhất trong danh sách hiện tại của trường
            worst_student = min(current_students, key=lambda x: scores[x])
            
            if scores[s] > scores[worst_student]:
                # Thí sinh mới có điểm cao hơn, thay thế thí sinh có điểm thấp nhất
                matches[u].remove(worst_student)
                matches[u].append(s)
                rejected_students.discard(s)  # Sinh viên đã được nhận
                free_students.append(worst_student)
                rejected_students.add(worst_student)  # Thí sinh bị thay thế trở thành rejected
            else:
                # Thí sinh mới có điểm không cao hơn, giữ nguyên danh sách
                free_students.append(s)
    
    return matches, list(rejected_students)

# Ví dụ về dữ liệu đầu vào
students = ['S1', 'S2', 'S3', 'S4']
scores = {'S1': 90, 'S2': 80, 'S3': 85, 'S4': 70}
university_capacities = {'U1': 1, 'U2': 2, 'U3': 1}
student_preferences = {
    'S1': ['U1', 'U2', 'U3'],
    'S2': ['U2', 'U3', 'U1'],
    'S3': ['U1', 'U3', 'U2'],
    'S4': ['U3', 'U2', 'U1']
}

matches, rejected_students = stable_matching_with_scores(students, scores, university_capacities, student_preferences)

print("Kết quả ghép đôi ổn định:")
for u, s in matches.items():
    print(f"Trường {u}: {', '.join(s)}")

print("\nDanh sách sinh viên không đỗ:")
print(", ".join(rejected_students))
