
# This program is to move expired files to a specific archive folder
# Delete them after a regular period

import os
import re
import shutil
import zipfile
import time
from datetime import datetime

source_path = "C:\original"
file_destination = "C:\_archive"
file_temp = file_destination + "\_temp"

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print
        "---  new folder...  ---"
    else:
        print
        "---  There is this folder!  ---"


#file_destination = "C:\_archive"
mkdir(file_destination)

#file_temp = "C:\_archive\_temp"
mkdir(file_temp)


pattern=re.compile(r'')

for root,dirs,files in os.walk(source_path):
    for name in files:

        file_path=os.path.join(root,name)
        #print(file_path)
        if pattern.search(file_path) is not None :
            ctime = time.localtime(os.path.getctime(file_path))
            filetime = time.strftime("%Y-%m-%d %H:%M:%S", ctime)
            start = datetime.strptime(filetime,"%Y-%m-%d %H:%M:%S")
            #print(start)

            currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current = datetime.strptime(currenttime,"%Y-%m-%d %H:%M:%S")
            #print(current)

            timedelta = (current-start)
            #print(timedelta.seconds)

            if timedelta.seconds > 604800:
                shutil.move(file_path, file_temp)
            #if timedelta.seconds > 30:
                #shutil.move(file_path, file_temp)

# create the zip and copy all the files from the temp
if not os.listdir(file_temp):
    pass
else:
    zip_name = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    zip_file_name = file_destination+"\\"+str(zip_name)+".zip"
    zip_file=zipfile.ZipFile(zip_file_name,'w')

    with zip_file:
        for temp_root, temp_dirs, temp_files in os.walk(file_temp):
            fpath = temp_root.replace(file_temp,'')
            for tozip_name in temp_files:
                zip_file.write(os.path.join(temp_root,tozip_name),os.path.join(fpath,tozip_name))

    zip_file.close()

shutil.rmtree(file_temp)

for ar_root,ar_dirs,ar_files in os.walk(file_destination):
    for ar_name in ar_files:
        #date_str = ar_name.replace('.zip','').split('-')

        file_ar_date = datetime.strptime(ar_name.replace('.zip',''),"%Y-%m-%d-%H-%M-%S")
        currenttime_ = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        current_ar_date = datetime.strptime(currenttime_, "%Y-%m-%d-%H-%M-%S")

        day_time_delta = (current_ar_date - file_ar_date)
        #print(day_time_delta.days)

        if day_time_delta.days > 180:
            current_zip_file = file_destination + "\\" + ar_name
            os.remove(current_zip_file)


