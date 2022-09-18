from Global_Varibles import *
from chinese_character import chinese_align
from common_func import *

import dir_dealing
import excel_read
import os


def add_work_type_into_all_student_folders_at_all_classified_folders(path_work_root, path_excel=None, ask_before_delete_illegal_naming_folder=True):
    if path_excel == None:
        path_excel_may_exist = os.path.dirname(
            path_work_root)  # 默认选择作品根目录的上一级文件夹
    path_excel = excel_read.look_for_scoring_excel(path_excel_may_exist)
    student_rank_data = excel_read.get_excel_student_data(path_excel)
    for root, dir, file in os.walk(path_work_root):
        # root的最后尾部就是分类文件夹,例如：xxx\xxx\__$_优秀
        # 每个分类文件夹中或者根目录中的文件夹处理
        if root.split("\\")[-1] in All_Classified_Folders_Name_List or root == path_work_root:
            for student_work_folder_name in dir:  # 各个学生文件夹
                err_str = is_legal_folder_name_without_type(
                    student_work_folder_name)
                if err_str == True:
                    stu_info = student_work_folder_name.split(
                        "-")  # 拆解学生信息[校区，年级，班级，姓名]
                    new_folder_name_with_type = stu_info[0]+"-"+stu_info[1]+"-"+stu_info[2] + \
                        "-" + \
                        student_rank_data[student_work_folder_name]["type"] + "-" +\
                        stu_info[3]
                    os.rename(root+"\\"+student_work_folder_name,
                              root+"\\"+new_folder_name_with_type)  # 重命名
                    print(f"  >> 命名已去掉课题类型 : ", chinese_align(student_work_folder_name, 25),
                          "===>>>", chinese_align(new_folder_name_with_type, 25))
                else:
                    err_str = is_legal_folder_name_with_type(
                        student_work_folder_name)
                    if err_str == True:
                        print("***命名已经加上了类型：", chinese_align(
                            student_work_folder_name, 25), " in ", root)
                    elif student_work_folder_name.startswith(prefix_of_folders):
                        print("***系统文件夹：", chinese_align(
                            student_work_folder_name, 15), " in ", root)
                    else:  # 不合法命名文件夹处理
                        print(err_str)
                        dir_dealing.delete_a_folder_with_warning(
                            root+"\\"+student_work_folder_name, err_str,
                            ask_on_nonempty_folder=ask_before_delete_illegal_naming_folder)


def remove_work_type_into_all_student_folders_at_all_classified_folders(path_work_root, ask_before_delete_illegal_naming_folder=True):
    for root, dir, file in os.walk(path_work_root):
        # root的最后尾部就是分类文件夹,例如：xxx\xxx\__$_优秀
        # 每个分类文件夹中或者根目录中的文件夹处理
        if root.split("\\")[-1] in All_Classified_Folders_Name_List or root == path_work_root:  # 每个分类文件夹
            for student_work_folder_name in dir:  # 各个学生文件夹
                err_str = is_legal_folder_name_with_type(
                    student_work_folder_name)
                if err_str == True:
                    stu_info = student_work_folder_name.split(
                        "-")  # 拆解学生信息[校区，年级，班级，类型，姓名]
                    new_folder_name_without_type = stu_info[0]+"-"+stu_info[1]+"-"+stu_info[2] + \
                        "-" + stu_info[4]
                    os.rename(root+"\\"+student_work_folder_name,
                              root+"\\"+new_folder_name_without_type)  # 重命名
                    print(f"  >> 命名已去掉课题类型 : ", chinese_align(student_work_folder_name, 25),
                          "===>>>", chinese_align(new_folder_name_without_type, 25))
                else:
                    err_str = is_legal_folder_name_without_type(
                        student_work_folder_name)
                    if err_str == True:
                        print("***命名已经去掉了类型：", chinese_align(
                            student_work_folder_name, 25), " in ", root)
                    elif student_work_folder_name.startswith(prefix_of_folders):
                        print("***系统文件夹：", chinese_align(
                            student_work_folder_name, 15), " in ", root)
                    else:  # 不合法命名文件夹处理
                        print(err_str)
                        dir_dealing.delete_a_folder_with_warning(
                            root+"\\"+student_work_folder_name, err_str,
                            ask_on_nonempty_folder=ask_before_delete_illegal_naming_folder)


remove_work_type_into_all_student_folders_at_all_classified_folders(
    'F:\_____科创作业汇总\上传作业电子版')
# root_path = 'F:\_____科创作业汇总\上传作业电子版'
# for root, dir, file in os.walk(root_path):
#     if root == root_path:
#         print(dir)
