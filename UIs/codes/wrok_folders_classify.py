from genericpath import isfile
import os
import sys
import re
import dir_dealing
import chinese_character
import excel_read
import win32api
from common_func import *
import win32con
from Global_Varibles import *


def make_all_campus_grade_class_rank_folders(path_work_root, directly_exit_if_exist=False, ask_before_delete_the_existed_folder=True):
    for campus in campus_grade_class_count.keys():
        path_campus = path_work_root+"\\"+prefix_of_folders+campus
        dir_dealing.make_a_folder_with_warning(path_campus, directly_exit_if_exist=directly_exit_if_exist,
                                               ask_before_delete_the_existed_folder=ask_before_delete_the_existed_folder)  # 校区文件夹
        for grade in campus_grade_class_count[campus].keys():
            path_grade = path_campus+"\\"+grade
            dir_dealing.make_a_folder_with_warning(path_grade, directly_exit_if_exist=directly_exit_if_exist,
                                                   ask_before_delete_the_existed_folder=ask_before_delete_the_existed_folder)  # 年级文件夹
            for class_n in range(1, campus_grade_class_count[campus][grade]+1):
                path_class = path_grade+"\\"+str(class_n)+"班"
                dir_dealing.make_a_folder_with_warning(path_class, directly_exit_if_exist=directly_exit_if_exist,
                                                       ask_before_delete_the_existed_folder=ask_before_delete_the_existed_folder)  # 班级文件夹
                for rank in rank_folders_name:
                    path_rank_folder = path_class+"\\"+rank
                    dir_dealing.make_a_folder_with_warning(
                        path_rank_folder, directly_exit_if_exist=directly_exit_if_exist, ask_before_delete_the_existed_folder=ask_before_delete_the_existed_folder)  # 班级文件夹


def make_invalid_and_unranked_folder(path_work_root, directly_exit_if_exist=False, ask_before_delete_the_existed_folder=True):
    dir_dealing.make_a_folder_with_warning(path_work_root+"\\"+folder_name_invalid,
                                           directly_exit_if_exist=directly_exit_if_exist, ask_before_delete_the_existed_folder=ask_before_delete_the_existed_folder)
    dir_dealing.make_a_folder_with_warning(
        path_work_root+"\\"+folder_name_unrankd, directly_exit_if_exist=directly_exit_if_exist, ask_before_delete_the_existed_folder=ask_before_delete_the_existed_folder)


def extract_student_info_from_legal_student_folder(legal_folder_name):
    # 按照规则匹配文件夹名字
    result = re.match(
        regex_str_of_student_folder_without_type, legal_folder_name)
    if result:
        return result.groupdict()
    else:
        print("*********不是合法的文件夹名字：extract_student_info_from_legal_student_folder: ",
              legal_folder_name)
        return None


def sort_basis_list(folder_name):  # 文件名按照名称排序的依据：按照拼音首字母排序
    result = re.match(regex_str_of_student_folder_without_type, folder_name)
    if result:
        match_dict = result.groupdict()
        campus_ord_assending = chinese_character.single_get_first(
            match_dict["campus"][0])
        grade_ascending = int(match_dict["grade"][1])  # 提前数字
        class_ascending = int(match_dict["class_n"])
        pinying_assending_1 = chinese_character.single_get_first(
            match_dict["name"][0])
        pinying_assending_2 = chinese_character.single_get_first(
            match_dict["name"][1])
        return [campus_ord_assending, grade_ascending, class_ascending, pinying_assending_1, pinying_assending_2]
    else:
        return [0, 0, 0, 0, 0]

#todo: 增加入选带类型的文件夹
# 过滤合法命名的学生文件夹，但是可能不在登记表中


def filter_legal_naming_student_work_folder_at_root_folder(path_work_root, ask_delete_on_nonempty_folder=True):
    print(separater_func_begin+" @ "+sys._getframe().f_code.co_name)
    print("筛选合法的学生文件夹......")

    all_files_and_folders_in_root_path = os.listdir(path_work_root)
    filtered_legal_students_folder_list = []
    for fils_or_folder in all_files_and_folders_in_root_path:
        # 判断是否合法命名,初步判断命名
        if os.path.isdir(path_work_root+"\\"+fils_or_folder):
            if fils_or_folder.startswith(prefix_of_folders):
                print("系统分类文件夹：", fils_or_folder)
                continue
            err_str = is_legal_folder_name_without_type(
                fils_or_folder)
            if err_str == True:
                filtered_legal_students_folder_list.append(fils_or_folder)
            else:
                dir_dealing.delete_a_folder_with_warning(
                    path_work_root+"\\"+fils_or_folder, err_str,
                    ask_on_nonempty_folder=ask_delete_on_nonempty_folder)
    filtered_legal_students_folder_list.sort(
        key=sort_basis_list)  # 模拟windows给文件名升序
    print("完成！")
    print(separater_func_end)
    return filtered_legal_students_folder_list


# 清除根目录中的不合法命名文件夹
def delete_all_illegal_namimg_student_folders(path_work_root, ask_delete_on_nonempty_folder=True):
    filter_legal_naming_student_work_folder_at_root_folder(
        path_work_root, ask_delete_on_nonempty_folder)


# 清除根目录中的不合法、无效、信息缺失的文件夹
def delete_all_illega_and_invalid_and_non_excel_registered_student_folders_at_work_root(path_work_root, path_excel=None, delete_invalid=False, ask_on_nonempty_folder=True):
    print(separater_func_begin+" @ "+sys._getframe().f_code.co_name)
    print("清除不合法、无效、信息缺失的文件夹......")
    if path_excel == None:
        path_excel_may_exist = os.path.dirname(
            path_work_root)  # 默认选择作品根目录的上一级文件夹
    path_excel = excel_read.look_for_scoring_excel(path_excel_may_exist)
    student_rank_data = excel_read.get_excel_student_data(path_excel)
    filtered_legal_students_folder_list = filter_legal_naming_student_work_folder_at_root_folder(
        path_work_root, ask_delete_on_nonempty_folder=ask_on_nonempty_folder)  # 选出合法文件夹,并删除不合法命名的文件夹

    for students_folder in filtered_legal_students_folder_list:
        path_src = path_work_root+"\\"+students_folder  # 每一个学生文件夹
        # 作品根目录中查找所有学生文件夹
        match_dict = extract_student_info_from_legal_student_folder(
            students_folder)
        if students_folder not in student_rank_data.keys():  # excel中没有该学生信息
            print("文件信息错误:  excel表中无此信息--->>", students_folder)
            dir_dealing.delete_a_folder_with_warning(
                path_src, warning_str_ahead=f'excel表中无"{ match_dict["name"]}"同学信息!!\n是否删除？？', ask_on_nonempty_folder=ask_on_nonempty_folder)  # 询问删除
        else:  # 找到了信息
            # 上传信息错误，无效
            if delete_invalid and student_rank_data[students_folder]["valid"] == False:
                print("文件无效:  excel表中此同学班级信息矛盾--->>", students_folder)
                deleted = dir_dealing.delete_a_folder_with_warning(
                    path_src, warning_str_ahead=f'excel表中第 {student_rank_data[students_folder]["line"]} 行  \"{ students_folder }\"  同学班级信息矛盾!!\n可能家长不确定班级, 是否删除？？', ask_on_nonempty_folder=True)  # 询问删除
                if not deleted:
                    show = win32api.MessageBox(
                        0, f"是否查看  \"{students_folder}\"  联系方式？？", "提醒", win32con.MB_YESNO)
                    if show == win32con.IDYES:
                        win32api.MessageBox(
                            0, f'\"{students_folder}\"  同学联系方式电话: {student_rank_data[students_folder]["phone"]}', "提醒", win32con.MB_OK)
    print("完成！")
    print(separater_func_end)


def classify_all_student_work_folders(path_work_root, path_excel=None):
    print(separater_func_begin+" @ "+sys._getframe().f_code.co_name)
    print("将学生文件夹归类到对应的等级文件夹中...")
    if path_excel == None:
        path_excel_may_exist = os.path.dirname(
            path_work_root)  # 默认选择作品根目录的上一级文件夹
    path_excel = excel_read.look_for_scoring_excel(path_excel_may_exist)
    student_rank_data = excel_read.get_excel_student_data(path_excel)
    filtered_legal_students_folder_list = filter_legal_naming_student_work_folder_at_root_folder(
        path_work_root)  # 选出合法文件夹
    n_not_rankd = 0
    n_moved = 0

    for students_folder in filtered_legal_students_folder_list:
        path_src = path_work_root+"\\"+students_folder  # 每一个学生文件夹
        # 作品根目录中查找所有学生文件夹
        match_dict = extract_student_info_from_legal_student_folder(
            students_folder)
        if students_folder not in student_rank_data.keys():  # excel中没有该学生信息
            print("文件信息错误:  excel表中无此信息--->>", students_folder)
            dir_dealing.delete_a_folder_with_warning(
                path_work_root+"\\"+students_folder, warning_str_ahead=f'excel表中无"{ match_dict["name"]}"同学信息!!\n是否删除？？')  # 删除
        else:  # 找到了信息
            if student_rank_data[students_folder]["valid"] == True:  # 上传信息正确，有效
                if student_rank_data[students_folder]["rank"] == "":  # 还未评级
                    print("文件信息提示:  学生作品还未评级--->>",
                          students_folder, ", 已经移动到'未评级'文件夹")
                    n_not_rankd += 1
                    path_des = path_work_root+"\\"+folder_name_unrankd
                    dir_dealing.move_folder_with_warning(
                        path_src, path_des)
                else:  # 已经评级且有效
                    path_des = path_work_root+"\\" + prefix_of_folders+match_dict["campus"]+"\\" + match_dict["grade"] + \
                        "\\" + match_dict["class_n"] + "班\\" + prefix_of_folders + \
                        student_rank_data[students_folder]["rank"]
                    n_moved += 1
                    print(f"  >> 已分类 {n_moved}: ", chinese_character.chinese_align(students_folder, 30),
                          "===>>>", chinese_character.chinese_align(path_des.strip(path_work_root), 30))
                    dir_dealing.move_folder_with_warning(
                        path_src, path_des)
            else:  # 上传信息错误，无效
                print("文件无效:  excel表中此同学信息矛盾--->>", students_folder)
                path_des = path_work_root+"\\"+folder_name_invalid
                dir_dealing.move_folder_with_warning(
                    path_src, path_des)
    if n_not_rankd != 0:
        win32api.MessageBox(0, str(n_not_rankd)+"个同学还没有被评等级\n请打开登记表查看~",
                            "提醒", win32con.MB_OK)
    if n_moved:
        print("完成！")
    else:
        print("没有学生作品文件夹需要归类~~")
    print(separater_func_end)


# 归类
classify_all_student_work_folders(
    'F:\_____科创作业汇总\上传作业电子版')


# 新建XXXX空的   等级文 你慢慢件夹
# make_all_campus_grade_class_rank_folders(
#     'F:\_____科创作业汇总\上传作业电子版', False, False)
