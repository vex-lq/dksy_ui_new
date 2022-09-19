import os
from codex.common_func import *
from codex.chinese_character import *
import codex.excel_read as excel_read
import codex.dir_dealing as dir_dealing
import codex.wrok_folders_classify as wrok_folders_classify

# 根目录或者所有归类目录中的作品文件夹，添加或删除命名中的作品类型type


def add_or_remove_work_type_into_all_student_folders_at_all_classified_folders(path_work_root, add_or_delete_type=True, path_excel=None, ask_before_delete_illegal_naming_folder=True):
    # 读取excel中的type信息:添加需要类型信息，删除也需要人员信息，查看是否在列表
    if path_excel == None:
        path_excel_may_exist = os.path.dirname(
            path_work_root)  # 默认选择作品根目录的上一级文件夹
        path_excel = excel_read.look_for_scoring_excel(path_excel_may_exist)
    student_rank_data = excel_read.get_excel_student_data(path_excel)

    if add_or_delete_type == True:  # 添加
        act_str = "添加"
        get_err_reason_of_folder_name_first = get_err_reason_of_folder_name_with_no_type
        get_err_reason_of_folder_name_then = get_err_reason_of_folder_name_with_type
    else:
        act_str = "删除"
        get_err_reason_of_folder_name_first = get_err_reason_of_folder_name_with_type
        get_err_reason_of_folder_name_then = get_err_reason_of_folder_name_with_no_type

    for root, dir, file in os.walk(path_work_root):
        # root的最后尾部就是分类文件夹,例如：xxx\xxx\__$_优秀
        # 每个分类文件夹中或者根目录中的文件夹处理
        if root.split("\\")[-1] in Global_Varibles.All_Classified_Folders_Name_List or root == path_work_root:
            for student_work_folder_name in dir:  # 各个学生文件夹
                err_str = get_err_reason_of_folder_name_first(
                    student_work_folder_name)
                if err_str == None:  # 判断是否有类型或者是无类型
                    stu_info = student_work_folder_name.split("-")  # 拆解学生信息
                    if add_or_delete_type:  # 添加类型
                        # 不带类型的合法命名：[校区，年级，班级，姓名]
                        student_idx = student_work_folder_name
                        if student_idx not in student_rank_data.keys():  # 名字合法但是excel表无信息
                            dir_dealing.delete_a_folder_with_warning(
                                root+"\\"+student_work_folder_name, warning_str_ahead='excel表中无此同学信息', ask_on_nonempty_folder=True)
                        else:
                            new_folder_name = stu_info[0]+"-"+stu_info[1]+"-"+stu_info[2] + \
                                "-" + \
                                student_rank_data[student_work_folder_name]["type"] + "-" +\
                                stu_info[3]
                    else:  # 删除类型
                        # 带类型的合法命名：[校区，年级，班级，类型，姓名]
                        student_idx = stu_info[0]+"-"+stu_info[1]+"-"+stu_info[2] + \
                            "-" + stu_info[4]
                        if student_idx not in student_rank_data.keys():  # 名字合法但是excel表无信息
                            dir_dealing.delete_a_folder_with_warning(
                                root+"\\"+student_work_folder_name, warning_str_ahead='excel表中无此同学信息', ask_on_nonempty_folder=True)
                        else:
                            new_folder_name = student_idx
                    print(student_work_folder_name)
                    # 重命名
                    os.rename(root+"\\"+student_work_folder_name,
                              root+"\\"+new_folder_name)  # 重命名
                    print(f"  >> 已{act_str}掉课题类型 : ", chinese_align(student_work_folder_name, 20),
                          "===>>>", chinese_align(new_folder_name, 20))
                else:  # 判断是否已经添加（或者删除）
                    err_str = get_err_reason_of_folder_name_then(
                        student_work_folder_name)
                    if err_str == None:
                        match_dict = wrok_folders_classify.extract_student_info_with_no_type_from_legal_student_folder(
                            student_work_folder_name)
                        student_idx = match_dict["campus"]+"-" + \
                            match_dict["grade"]+"-"+match_dict["class_n"] + \
                            "班-"+match_dict["name"]
                        if student_idx not in student_rank_data.keys():  # 名字合法但是excel表无信息
                            dir_dealing.delete_a_folder_with_warning(
                                root+"\\"+student_work_folder_name, warning_str_ahead='excel表中无此同学信息', ask_on_nonempty_folder=True)
                        else:
                            print(f"***原文件夹命名已经{act_str}了类型：", chinese_align(
                                student_work_folder_name, 20), " in ", root)
                    elif student_work_folder_name.startswith(Global_Varibles.prefix_of_folders):
                        print("***系统文件夹：", chinese_align(
                            student_work_folder_name, 15), " in ", root)
                    else:  # 不合法命名文件夹处理
                        print("xxxxxxxxxxxxxxxxxxxxx",err_str)
                        dir_dealing.delete_a_folder_with_warning(
                            root+"\\"+student_work_folder_name, err_str,
                            ask_on_nonempty_folder=ask_before_delete_illegal_naming_folder)
