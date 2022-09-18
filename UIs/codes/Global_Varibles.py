import sys

# 归类文件夹前缀
prefix_of_folders = "__$_"

# 校区和年级
All_Campus = ['天骄', '清水河', '尚丰']
All_Grades = ["高1", "高2", "初1", "初2"]
All_Work_Types = ["发明", "论文", "科幻画", "科学影像", "理化生实验改进"]

All_Campus_Folders_Names = [prefix_of_folders+c for c in All_Campus]
All_Grades_Folders_Names=All_Grades

# 每个校区年级的班级数量字典
campus_grade_class_count = {}
campus_grade_class_count["清水河"] = {}
campus_grade_class_count["天骄"] = {}
campus_grade_class_count["尚丰"] = {}
# 年级的班级总数量设置
campus_grade_class_count["清水河"]["高1"] = 15
campus_grade_class_count["清水河"]["高2"] = 15
campus_grade_class_count["天骄"]["初1"] = 15
campus_grade_class_count["天骄"]["初2"] = 15
campus_grade_class_count["尚丰"]["初1"] = 15
campus_grade_class_count["尚丰"]["初2"] = 15

# 等级文件夹名字
Rank_Folder_Names = [
    prefix_of_folders + "优秀",
    prefix_of_folders + "良好",
    prefix_of_folders + "合格",
    prefix_of_folders + "不合格",
]
# 无效和未评级的文件夹名字
Invalid_Folder_Name = prefix_of_folders+"无效上传"
Unrankd_Folder_Name = prefix_of_folders+"未评等级"
# 所有的分类文件夹
All_Classified_Folders_Name_List = Rank_Folder_Names + \
    [Invalid_Folder_Name, Unrankd_Folder_Name]

# 学生姓名匹配规则
regex_student_name_chinese_only = r"([\u4e00-\u9fa5]{2,4})$"  # 学生名字：2到4个中文汉字
# 学生名字：2到4个汉字,或者2到40个英文字母
regex_student_name_english_too = r"([\u4e00-\u9fa5]{2,4}|\D{2,40})$"


STUDENT_NAME_USING_ENGLISH = False
if STUDENT_NAME_USING_ENGLISH:
    regex_student_name = regex_student_name_english_too
else:
    regex_student_name = regex_student_name_chinese_only

# 初步匹配学生文件夹名
rough_regex_of_student_folder_with_no_type = r"(?P<campus>(\D)+)-(?P<grade>[高初][\d]+)-(?P<class_n>[\d]+)班-(?P<name>(.)+)$"
rough_regex_of_student_folder_with_type = r"(?P<campus>(\D)+)-(?P<grade>[高初][\d]+)-(?P<class_n>[\d]+)班-(?P<type>(\D)+)-(?P<name>(.)+)$"

# 初步匹配学生文件夹名
if STUDENT_NAME_USING_ENGLISH:
    exact_regex_of_student_folder_with_no_type = r"(?P<campus>(\D)+)-(?P<grade>[高初][\d]+)-(?P<class_n>[\d]+)班-(?P<name>[\u4e00-\u9fa5]{2,4}|[a-zA-Z]{2,40})$"
    exact_regex_of_student_folder_with_type = r"(?P<campus>(\D)+)-(?P<grade>[高初][\d]+)-(?P<class_n>[\d]+)班-(?P<type>[\u4e00-\u9fa5]+)-(?P<name>[\u4e00-\u9fa5]{2,4}|[a-zA-Z]{2,40})$"
else:
    exact_regex_of_student_folder_with_no_type = r"(?P<campus>[\u4e00-\u9fa5]{2,3})-(?P<grade>[高初][\d]+)-(?P<class_n>[\d]+)班-(?P<name>[\u4e00-\u9fa5]{2,4})$"
    exact_regex_of_student_folder_with_type = r"(?P<campus>[\u4e00-\u9fa5]{2,3})-(?P<grade>[高初][\d]+)-(?P<class_n>[\d]+)班-(?P<type>[\u4e00-\u9fa5]+)-(?P<name>[\u4e00-\u9fa5]{2,4})$"


separater_func_begin = "begin------------------------------------------------"
separater_func_end = "end-------------------------------------------------\n\n"
