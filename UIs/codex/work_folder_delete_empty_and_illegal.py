import codex.Global_Varibles as Global_Varibles
import codex.dir_dealing as dir_dealing
from codex.common_func import *
import os

# 清除空的归类文件夹和cgc文件夹


def delete_empty_classify_and_cgc_folder(path_work_root):
    for local_root, folders, files in os.walk(path_work_root):
        # root的最后尾部就是分类文件夹,例如：xxx\xxx\__$_优秀
        if local_root.split("\\")[-1] in Global_Varibles.All_Classified_Folders_Name_List:
            if folders == []:  # 删除没有学生作品文件夹的归类文件夹
                dir_dealing.delete_a_folder_with_warning(local_root)
    # 计算根目录的层级数
    folder_n_level_path_work_root = len(path_work_root.split("\\"))
    for local_root, folders, file in os.walk(path_work_root, topdown=False):
        cgc_folder = False  # 校区、年级、班级文件夹
        if len(local_root.split("\\")) == folder_n_level_path_work_root+3:
            cgc_folder = True  # 班级文件夹
        elif len(local_root.split("\\")) == folder_n_level_path_work_root+2 and local_root.split("\\")[-2] not in Global_Varibles.All_Classified_Folders_Name_List:
            cgc_folder = True  # 年级文件夹
        elif len(local_root.split("\\")) == folder_n_level_path_work_root+1 and local_root.split("\\")[-1] not in Global_Varibles.All_Classified_Folders_Name_List:
            cgc_folder = True  # 校区文件夹
        if cgc_folder and folders == []:  # 依次删除空的班级、年级、校区文件夹
            dir_dealing.delete_a_folder_with_warning(local_root)


# 判断一个文件夹是否合法，并删除
def delete_illegal_folder(path_work_root, folder, upper_path, where="", ask_on_nonempty_folder=True):
    # 不合法
    if not (get_err_reason_of_folder_name_with_no_type(folder) == None or get_err_reason_of_folder_name_with_type(folder) == None):
        if folder in Global_Varibles.All_Classified_Folders_Name_List:
            choice = warn_messagebox(
                f'{where}发现一个系统分类的文件夹:\n{upper_path}\n\"{folder}\"\n\n是否移到"根目录{path_work_root}"文件夹中？', win32con.MB_ICONWARNING | win32con.MB_YESNO)
            if choice:
                print("move")
                dir_dealing.move_a_folder_with_warning(
                    upper_path+"\\"+folder, path_work_root, directly_exit_if_exist=False, ask_before_delete_nonempty_des_folder=True)
        else:
            return dir_dealing.delete_a_folder_with_warning(
                upper_path+"\\"+folder, warning_str_ahead=f'{where}发现一个命名不合法的学生文件夹:\n{upper_path}\n\"{folder}\"\n\n是否删除？', ask_on_nonempty_folder=ask_on_nonempty_folder)
    else:  # 合法
        choice = warn_messagebox(
            f'{where}发现一个命名合法的学生文件夹:\n{upper_path}\n\"{folder}\"\n\n是否移到"{Global_Varibles.prefix_of_folders}未评等级"文件夹中？', win32con.MB_ICONWARNING | win32con.MB_YESNO)
        if choice:
            dir_dealing.move_a_folder_with_warning(upper_path+"\\"+folder, path_work_root+"\\"+Global_Varibles.prefix_of_folders +
                                                   "未评等级", directly_exit_if_exist=False, ask_before_delete_nonempty_des_folder=True)

# 检查根目录和归类文件中，学生作品文件夹命名是否合法并删除


def check_and_delete_all_student_work_folders_at_root_and_classify_folders(path_work_root, ask_on_nonempty_folder=True):
    for local_root, folders, files in os.walk(path_work_root):
        # 遍历所有归类文件夹
        if local_root.split("\\")[-1] in Global_Varibles.All_Classified_Folders_Name_List:
            for work_folder in folders:
                # 归类文件夹中的作品文件夹命名不合法
                delete_illegal_folder(path_work_root,
                                      work_folder, local_root, where="分类文件夹中", ask_on_nonempty_folder=ask_on_nonempty_folder)

        if local_root == path_work_root:  # 根目录文件夹
            for work_folder in folders:
                if not work_folder.startswith(Global_Varibles.prefix_of_folders):
                    delete_illegal_folder(path_work_root,
                                          work_folder, local_root, where="根目录文件夹中", ask_on_nonempty_folder=ask_on_nonempty_folder)


def delete_files_list(local_root, files):
    for file in files:
        os.remove(local_root+"\\"+file)


# 清除cgc文件夹中的未知文件、不合法文件夹


def clear_all_unknown_cgc_folders(path_work_root, ask_on_nonempty_folder=True):
    # 计算根目录的层级数
    folder_n_level_path_work_root = len(path_work_root.split("\\"))
    for local_root, folders, files in os.walk(path_work_root, topdown=True):
        if len(local_root.split("\\")) == folder_n_level_path_work_root:  # 在根目录
            for folder in folders:  # 各个校区文件夹
                if folder not in Global_Varibles.All_Classified_Folders_Name_List and folder not in Global_Varibles.All_Campus_Folders_Names:
                    delete_illegal_folder(path_work_root,
                                          folder, local_root, where="根目录文件夹中", ask_on_nonempty_folder=ask_on_nonempty_folder)
            delete_files_list(local_root, files)  # 删除文件
        elif len(local_root.split("\\")) == folder_n_level_path_work_root+1:  # 在校区文件夹
            for folder in folders:  # 各个年级文件夹
                if not re.match("[高初][12]$", folder) and local_root.split("\\")[-1] not in Global_Varibles.All_Classified_Folders_Name_List:
                    delete_illegal_folder(path_work_root,
                                          folder, local_root, where="校区文件夹中", ask_on_nonempty_folder=ask_on_nonempty_folder)
            delete_files_list(local_root, files)
        elif len(local_root.split("\\")) == folder_n_level_path_work_root+2:  # 在年级文件夹
            for folder in folders:  # 各个班级文件夹
                if not re.match("(\d){1,2}班$", folder) and re.match("[高初][12]$", local_root.split("\\")[-1]):
                    delete_illegal_folder(path_work_root,
                                          folder, local_root, where="年级文件夹中", ask_on_nonempty_folder=ask_on_nonempty_folder)
            delete_files_list(local_root, files)
        elif len(local_root.split("\\")) == folder_n_level_path_work_root+3:  # 在班级文件夹
            for folder in folders:  # 各个等级归类文件夹
                if folder not in Global_Varibles.Rank_Folder_Names and re.match("(\d){1,2}班$", local_root.split("\\")[-1]):
                    delete_illegal_folder(path_work_root,
                                          folder, local_root, where="班级文件夹中", ask_on_nonempty_folder=ask_on_nonempty_folder)
            delete_files_list(local_root, files)


# 删除空cgc和归类文件夹
# delete_empty_classify_and_cgc_folder('F:\_____科创作业汇总\上传作业电子版')

# 根目录和归类文件夹中检测不合法学生文件夹
# check_and_delete_all_student_work_folders_at_root_and_classify_folders(
#     'F:\_____科创作业汇总\上传作业电子版')

# 清理未知的无关文件和文件夹
# clear_all_unknown_cgc_folders('F:\_____科创作业汇总\上传作业电子版')
