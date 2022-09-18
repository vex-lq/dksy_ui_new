import os
from Global_Varibles import *
import dir_dealing


# 删除所有的cgc文件夹
def delete_all_campus_grade_class_rank_folders(path_work_root, ask_on_nonempty_folder=True):
    for campus in campus_grade_class_count.keys():
        path_campus = path_work_root+"\\"+prefix_of_folders+campus
        dir_dealing.delete_a_folder_with_warning(
            path_campus, ask_on_nonempty_folder=ask_on_nonempty_folder)  # 校区文件夹
        for grade in campus_grade_class_count[campus].keys():
            path_grade = path_campus+"\\"+grade
            dir_dealing.delete_a_folder_with_warning(
                path_grade, ask_on_nonempty_folder=ask_on_nonempty_folder)  # 年级文件夹
            for class_n in range(1, campus_grade_class_count[campus][grade]+1):
                path_class = path_grade+"\\"+str(class_n)+"班"
                dir_dealing.delete_a_folder_with_warning(
                    path_class, ask_on_nonempty_folder=ask_on_nonempty_folder)  # 班级文件夹
                for rank in Rank_Folder_Names:
                    path_rank_folder = path_class+"\\"+rank
                    dir_dealing.delete_a_folder_with_warning(
                        path_rank_folder, ask_on_nonempty_folder=ask_on_nonempty_folder)  # 班级文件夹


# 删除未评级和未无效归类文件夹
def delete_invalid_and_unranked_folder(path_work_root, ask_on_nonempty_folder=True):
    dir_dealing.delete_a_folder_with_warning(
        path_work_root+"\\"+Invalid_Folder_Name, ask_on_nonempty_folder=ask_on_nonempty_folder)
    dir_dealing.delete_a_folder_with_warning(
        path_work_root+"\\"+Unrankd_Folder_Name, ask_on_nonempty_folder=ask_on_nonempty_folder)


# 取消归类,并删除（可选）所有cgc文件夹
def declassify_all_student_work_folders(path_work_root, delete_empty_classified_folders=True):
    for root, dir, file in os.walk(path_work_root):
        if root.split("\\")[-1] in All_Classified_Folders_Name_List:  # 遍历所有归类文件夹
            for work_folder in dir:
                # 直接替换
                dir_dealing.move_a_folder_with_warning(
                    root+"\\"+work_folder, path_work_root, directly_exit_if_exist=False, ask_replace_the_existed_folder=False)
    if delete_empty_classified_folders:
        delete_all_campus_grade_class_rank_folders(
            path_work_root, ask_on_nonempty_folder=False)
        delete_invalid_and_unranked_folder(
            path_work_root, ask_on_nonempty_folder=False)


declassify_all_student_work_folders(
    'F:\_____科创作业汇总\上传作业电子版', delete_empty_classified_folders=True)
