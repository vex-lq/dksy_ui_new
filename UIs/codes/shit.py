import os
from Global_Varibles import *


for root, dir, file in os.walk('F:\_____科创作业汇总\上传作业电子版\__$_尚丰', topdown=False):
    if root.split("\\") in All_Classified_Folders_Name_List:
        print(root, dir)


#修改测试
#################