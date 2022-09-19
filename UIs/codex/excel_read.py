import xlrd
import os
import win32ui
import win32api
import win32con
from codex import common_func


def map_col_letters_to_int(string):  # excel的字目列转换成数字
    if string == "":
        return 0
    string = string.upper()
    if len(string) == 1:
        return ord(string)-ord('A')
    else:
        n = 0
        sum = 0
        for c in string[:-1]:
            n += 1
            sum += (ord(c)-ord('A')+1)*26 ** (len(string)-n)
        sum += ord(string[-1])-ord('A')
        return sum


def get_excel_student_data(path_excel):
    col_name = 'e'
    col_campus = 'g'
    col_grade_h = 'h'
    col_grade_m = 'i'
    col_class = 'j'
    col_check = 'k'
    col_rank = 'x'
    col_phone = 'u'
    col_type = 'm'

    book = xlrd.open_workbook(path_excel)
    sheet = book.sheet_by_index(0)  # 整张工作表

    all_names = sheet.col_values(map_col_letters_to_int(col_name))
    all_campus = sheet.col_values(map_col_letters_to_int(col_campus))
    all_grades_h = sheet.col_values(map_col_letters_to_int(col_grade_h))
    all_grades_m = sheet.col_values(map_col_letters_to_int(col_grade_m))
    all_class = sheet.col_values(map_col_letters_to_int(col_class))
    all_check = sheet.col_values(map_col_letters_to_int(col_check))
    all_rank = sheet.col_values(map_col_letters_to_int(col_rank))
    all_phone = sheet.col_values(map_col_letters_to_int(col_phone))
    all_type = sheet.col_values(map_col_letters_to_int(col_type))

    info_dict = {}
    for n in range(1, len(all_check)):
        idx = all_check[n]+"-"+all_names[n]
        info_dict[idx] = {}  # 构造各学生字典
        info_dict[idx]["rank"] = all_rank[n]  # 等级
        info_dict[idx]["line"] = n+1  # excel所在行
        info_dict[idx]["phone"] = all_phone[n]  # 联系电话
        info_dict[idx]["type"] = all_type[n]  # 作品类型

        if all_campus[n]+"-"+all_grades_h[n]+all_grades_m[n]+"-"+all_class[n] == all_check[n]:
            info_dict[idx]["valid"] = True  # 构造各学生字典
        else:
            info_dict[idx]["valid"] = False  # 构造各学生字典

    return info_dict


def look_for_scoring_excel(path_whole_root):  # 查找excel登记表
    files = os.listdir(path_whole_root)
    excel_files = []
    for file in files:
        # 不是文件夹，或者不是excel表
        if not os.path.isfile(path_whole_root+"\\"+file) or not file.endswith(".xlsx"):
            continue
        if file.startswith("~$"):  # wps或者office的同文件夹临时缓存文件
            continue
        excel_files.append(file)  # ok,添加进去
    if len(excel_files) == 0:
        if common_func.warn_messagebox("未找到学生等级登记表,是否添加？", win32con.MB_ICONWARNING | win32con.MB_YESNO):
            dlg = win32ui.CreateFileDialog(1)  # 打开文件
            dlg.SetOFNInitialDir(path_whole_root)
            flag = dlg.DoModal()
            if 1 == flag:
                return dlg.GetPathName()
            else:
                return None
        else:
            return None
    elif len(excel_files) == 1:
        return path_whole_root+"\\"+excel_files[0]
    else:
        if common_func.warn_messagebox(f"存在多个excel表:{excel_files}\n请选择1个学生等级登记表？", win32con.MB_ICONWARNING | win32con.MB_YESNO):
            dlg = win32ui.CreateFileDialog(1)  # 打开文件
            dlg.SetOFNInitialDir(path_whole_root)
            flag = dlg.DoModal()
            if 1 == flag:
                return dlg.GetPathName()
            else:
                return None
        else:
            return files
