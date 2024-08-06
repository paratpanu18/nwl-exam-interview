def is_valid_student_id(student_id: str) -> bool:
    return len(student_id) == 8 and student_id.isdigit() and student_id[0] == '6' and student_id[2:4] == '01'