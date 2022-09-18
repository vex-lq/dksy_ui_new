from Global_Varibles import *
from chinese_character import chinese_align
from common_func import *

import dir_dealing
import os


def delete_empty_classify_and_cgc_folder(path_work_root):
    for root, dir, file in os.walk(path_work_root):
        # root的最后尾部就是分类文件夹,例如：xxx\xxx\__$_优秀
        if root.split("\\")[-1] in All_Classified_Folders_Name_List:
            if dir == []:  # 删除没有学生作品文件夹的归类文件夹
                dir_dealing.delete_a_folder_with_warning(root)
    # 计算根目录的层级数
    folder_n_level_path_work_root = len(path_work_root.split("\\"))
    for root, dir, file in os.walk(path_work_root, topdown=False):
        cgc_folder = False  # 校区、年级、班级文件夹
        if len(root.split("\\")) == folder_n_level_path_work_root+3:
            cgc_folder = True  # 班级文件夹
        elif len(root.split("\\")) == folder_n_level_path_work_root+2 and root.split("\\")[-2] not in All_Classified_Folders_Name_List:
            cgc_folder = True  # 年级文件夹
        elif len(root.split("\\")) == folder_n_level_path_work_root+1 and root.split("\\")[-1] not in All_Classified_Folders_Name_List:
            cgc_folder = True  # 校区文件夹
        if cgc_folder and dir == []:  # 依次删除空的班级、年级、校区文件夹
            dir_dealing.delete_a_folder_with_warning(root)


delete_empty_classify_and_cgc_folder('F:\_____科创作业汇总\上传作业电子版')
