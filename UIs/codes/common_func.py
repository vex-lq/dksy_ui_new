import win32api
import win32con
import re
from Global_Varibles import *


def warn_messagebox(warning_str, win32con_type):
    choice = win32api.MessageBox(0, warning_str,
                                 "提醒", win32con_type)
    if choice == win32con.IDYES:
        return True
    else:
        return False


# 注意，如果不合法，会返回错误原因字符串，正确才返回True,判断正确必须和True比较
def get_err_reason_of_folder_name_with_no_type(folder_name):
    if folder_name.startswith(prefix_of_folders):
        return None
    result = re.match(
        rough_regex_of_student_folder_with_no_type, folder_name)
    err_str = ""
    if result:
        match_dict = result.groupdict()
        if match_dict["campus"] not in All_Campus:  # 校区错误
            err_str = f'不合法的学生文件夹命名：  {folder_name }\n《错误原因：科中没有\"{match_dict["campus"]}\"校区》'
        elif match_dict["grade"] not in All_Grades:  # 年级错误
            err_str = f'不合法的学生文件夹命名：  {folder_name }\n《错误原因：没有\"{match_dict["grade"]}\"年级》'
        # 校区年级错位
        elif (match_dict["campus"] in ["天骄", "尚丰"] and "高" in match_dict["grade"]) or (match_dict["campus"] == "清水河" and "初" in match_dict["grade"]):
            err_str = f'不合法的学生文件夹命名：  {folder_name} \n《错误原因：\"{match_dict["campus"]}\"校区 没有 \"{match_dict["grade"]}\"年级》'
        elif int(match_dict["class_n"]) > campus_grade_class_count[match_dict["campus"]][match_dict["grade"]]:
            err_str = f'不合法的学生文件夹命名：  {folder_name }\n《错误原因：\"{match_dict["campus"]}-{match_dict["grade"]}\" 没有 \"{match_dict["class_n"]}班\"》'
        elif not re.match(regex_student_name, match_dict["name"]):
            err_str = f'不合法的学生文件夹命名：  {folder_name }\n《错误原因： 不合法的学生中文名： \"{match_dict["name"]}\"》'

        # print(re.match(regex_student_name, match_dict["name"]).group())
        if err_str == "":  # 校区、年级、班级数字均正确
            return None
    else:
        err_str = f"不合法的学生文件夹命名：" + folder_name
    return err_str

# 注意，如果不合法，会返回错误原因字符串，正确或系统文件夹返回None


def get_err_reason_of_folder_name_with_type(folder_name):
    if folder_name.startswith(prefix_of_folders):
        return None
    result = re.match(
        rough_regex_of_student_folder_with_type, folder_name)
    if result:
        match_dict = result.groupdict()
        # 组成不含类型的命名
        info_without_type_naming = match_dict["campus"]+"-" + \
            match_dict["grade"]+"-"+match_dict["class_n"] + \
            "班-"+match_dict["name"]
        err_str = get_err_reason_of_folder_name_with_no_type(
            info_without_type_naming)
        if err_str == None:  # 基本信息正确
            if match_dict["type"] in All_Work_Types:  # 类型也正确
                return None
            else:
                err_str = f'不合法的学生文件夹命名：  {folder_name }\n《错误原因： 不合法的作品类型： \"{match_dict["type"]}\"》'
                return err_str
        else:
            return err_str
    else:
        return f'完全不合法的学生文件夹命名'


# print(get_err_reason_of_folder_name_with_type("清水河-高1-10班-发明-王虎"))
