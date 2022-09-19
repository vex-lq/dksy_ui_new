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
    return os.path.dirname(string)+"\【<"+string.split("\\")[-1]+">】"


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
    return True  # 已删除


# 剪切文件夹:src_student_work_path---需要移动的文件夹； des_parent_folder_path--最终目标位置的上一级文件夹
def move_a_folder_with_warning(src_student_work_path, des_parent_folder_path, directly_exit_if_exist=True, ask_before_delete_nonempty_des_folder=True):  # 剪切文件夹
    src_aim_folder = src_student_work_path.split("\\")[-1]
    final_des_path = des_parent_folder_path + \
        "\\" + src_aim_folder  # 最终移动后的文件夹
    warning_str = f"移动文件夹:  【<{src_aim_folder}>】\n从: " + \
        add_line_to_folder_path(os.path.abspath(src_student_work_path))+"\n到: " + \
        add_line_to_folder_path(os.path.abspath(
            final_des_path))+"\n\n"

    if not os.path.exists(src_student_work_path):
        win32api.MessageBox(0, warning_str+"不存在:  "+add_line_to_folder_path(os.path.abspath(src_student_work_path)),
                            "提醒", win32con.MB_ICONWARNING)
        return False

    if not os.path.isdir(src_student_work_path):
        win32api.MessageBox(0, warning_str+"不是文件夹:  "+add_line_to_folder_path(os.path.abspath(src_student_work_path)),
                            "提醒", win32con.MB_ICONWARNING)
        return False

    if not os.path.exists(src_student_work_path):
        win32api.MessageBox(0, warning_str+"文件夹:  "+add_line_to_folder_path(os.path.abspath(src_student_work_path))+"\n不存在！",
                            "提醒", win32con.MB_ICONWARNING)
        return False

    if os.path.exists(final_des_path):  # 已存在
        if directly_exit_if_exist:
            return
        if os.path.isdir(final_des_path):  # 已存在且是文件夹
            if len(os.listdir(final_des_path)) == 0:  # 目标文件夹为空
                os.rmdir(final_des_path)
                shutil.move(src_student_work_path, des_parent_folder_path)
            else:
                if ask_before_delete_nonempty_des_folder:
                    choice = win32api.MessageBox(0, warning_str+"目标文件夹:  "+add_line_to_folder_path(os.path.abspath(final_des_path)) +
                                                 f"\n已存在并含有文件{file_list_add_line_to_str(os.listdir(final_des_path))}是否删除这些文件夹并剪切过来？\
                                                    \n\n（1）是：删除目标文件夹并剪切      \n（2）否：合并到目标文件夹  \n（3）取消：取消剪切",
                                                 "提醒", win32con.MB_ICONWARNING | win32con.MB_YESNOCANCEL)
                    if choice == win32con.IDYES:  # 全部删除目标位置的文件夹并全剪切过去
                        print("删除已存在的目标文件夹...")
                        shutil.rmtree(final_des_path,
                                      ignore_errors=True)
                        shutil.move(src_student_work_path,
                                    des_parent_folder_path)
                    elif choice == win32con.IDNO:  # 不删除，则合并
                        print("合并文件夹...")
                        for fd in os.listdir(src_student_work_path):  # 只移动原文件夹中的子文件夹和文件
                            move_a_folder_with_warning(src_student_work_path+"\\"+fd,
                                                       final_des_path, directly_exit_if_exist=False,
                                                       ask_before_delete_nonempty_des_folder=True)
                            shutil.rmtree(src_student_work_path+"\\"+fd,  # 合并子目录后，删除空的子件夹
                                          ignore_errors=True)
                        shutil.rmtree(src_student_work_path,  # 合并后，删除空的原文件夹
                                      ignore_errors=True)
                        return False
                    else:
                        print("取消移动")
                else:  # 直接全部替换目标位置的旧文件夹
                    shutil.rmtree(final_des_path, ignore_errors=True)
                    shutil.move(src_student_work_path, des_parent_folder_path)
        else:  # 直接删除已有的目标文件<非文件夹>
            os.remove(final_des_path)
    else:  # 不存在
        os.makedirs(des_parent_folder_path, exist_ok=True)
        shutil.move(src_student_work_path, des_parent_folder_path)
