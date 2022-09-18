from genericpath import isdir
import os
import shutil
import win32api
import win32con


def file_list_add_line_to_str(files_list):
    str = "\n"
    for s in files_list:
        str += "    *******"+s+"\n"
    return str


def add_line_to_folder_path(string):
    return os.path.dirname(string)+"\\\n               "+string.split("\\")[-1]


def make_a_folder_with_warning(folder_path, directly_exit_if_exist=True, ask_before_delete_the_existed_folder=True):  # 建立1个文件夹
    if os.path.exists(folder_path):
        if directly_exit_if_exist:
            return
        file_list = os.listdir(folder_path)
        if len(file_list):
            if ask_before_delete_the_existed_folder:
                choice = win32api.MessageBox(0, "文件夹:  "+add_line_to_folder_path(os.path.abspath(folder_path))+f"\n其内部还有文件：{file_list_add_line_to_str(file_list)}\n是否删除？",
                                                "提醒", win32con.MB_ICONWARNING | win32con.MB_YESNO)
                if choice == win32con.IDYES:
                    shutil.rmtree(folder_path, ignore_errors=True)
                    os.mkdir(folder_path)
                else:
                    pass  # 不清空已存在的文件
            else:
                shutil.rmtree(folder_path, ignore_errors=True)
                os.mkdir(folder_path)
        else:  # 文件夹已存在，并为空文件夹
            print("exist empty")
            pass  # 空文件夹，不处理不清空
    else:
        os.mkdir(folder_path)


def delete_a_folder_with_warning(folder_path, warning_str_ahead="", ask_on_nonempty_folder=True):  # 删除1个文件夹
    if not os.path.isdir(folder_path):
        return False
    if os.path.exists(folder_path):
        file_list = os.listdir(folder_path)
        if len(file_list):
            if ask_on_nonempty_folder:
                choice = win32api.MessageBox(0, warning_str_ahead+"\n\n"+"文件夹:  "+add_line_to_folder_path(os.path.abspath(folder_path))+f"\n其内部还有文件：{file_list_add_line_to_str(file_list)}\n是否删除？",
                                             "提醒", win32con.MB_ICONWARNING | win32con.MB_YESNO)
                if choice == win32con.IDYES:
                    shutil.rmtree(folder_path, ignore_errors=True)  # 删除
                else:
                    return False  # 不删除
            else:  # 不问就直接删
                shutil.rmtree(folder_path, ignore_errors=True)  # 直接删除
        else:  # 存在，但是为空文件夹\
            shutil.rmtree(folder_path, ignore_errors=True)  # 直接删除空文件夹
    return True


def make_folders_with_warning(folder_path_list):  # 建立一些列文件夹
    for folder_path in folder_path_list:
        make_a_folder_with_warning(folder_path)


def delete_folders_with_warning(folder_path_list):  # 删除1系列个文件夹
    for folder_path in folder_path_list:
        delete_a_folder_with_warning(folder_path)


def move_folder_with_warning(src_student_work_path, des_classified_folder_path, directly_exit_if_exist=True, ask_replace_the_existed_folder=True):  # 剪切文件夹
    student_folder = src_student_work_path.split("\\")[-1]
    final_student_work_path = des_classified_folder_path + \
        "\\" + student_folder  # 最终移动后的文件夹
    warning_str = f"移动学生文件夹:  {student_folder}\n从: " + \
        add_line_to_folder_path(os.path.abspath(src_student_work_path))+"\n到: " + \
        add_line_to_folder_path(os.path.abspath(
            final_student_work_path))+"\n\n"

    if not os.path.isdir(src_student_work_path):
        win32api.MessageBox(0, warning_str+"不是文件夹:  "+add_line_to_folder_path(os.path.abspath(src_student_work_path)),
                            "提醒", win32con.MB_ICONWARNING)
        return False

    if not os.path.exists(src_student_work_path):
        win32api.MessageBox(0, warning_str+"学生作品文件夹:  "+add_line_to_folder_path(os.path.abspath(src_student_work_path))+"\n不存在！",
                            "提醒", win32con.MB_ICONWARNING)
        return False

    if os.path.exists(final_student_work_path):  # 已存在
        if directly_exit_if_exist:
            return

        if os.path.isdir(final_student_work_path):
            if ask_replace_the_existed_folder:
                choice = win32api.MessageBox(0, warning_str+"学生作品文件夹:  "+add_line_to_folder_path(os.path.abspath(final_student_work_path))+"\n已存在，是否删除旧的作业文件夹？",
                                             "提醒", win32con.MB_ICONWARNING | win32con.MB_YESNO)
                if choice == win32con.IDYES:  # 替换已存在的文件
                    shutil.rmtree(final_student_work_path, ignore_errors=True)
                    shutil.move(src_student_work_path,
                                des_classified_folder_path)
                else:
                    return False
            else:  # 直接替换
                shutil.rmtree(final_student_work_path, ignore_errors=True)
                shutil.move(src_student_work_path, des_classified_folder_path)
        else:
            os.remove(final_student_work_path)  # 直接删除同名文件
    else:  # 不存在
        os.makedirs(des_classified_folder_path, exist_ok=True)
        shutil.move(src_student_work_path, des_classified_folder_path)
