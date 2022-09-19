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


 