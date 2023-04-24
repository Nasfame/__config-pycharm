import os

import shutil

import sys

import platform

from datetime import datetime

sources = ["migrate.py", "git2", ".git/hooks/post-commit",
           "_windows", "_mac",
           "keymaps",
           "keymapFlags.xml", "abbrevs.xml", "editor-font.xml"  # "colors.scheme.xml",]
                                             "codestyles", "code.style.schemes.xml", "colors",
           "vcs.xml",
           "ide.general.xml",
           "log_highlighting.xml",
           "NewUIInfoService.xml",
           "advancedSettings.xml",
           ]
destinations = ["pycharm","goland" , "webstorm", "rubymine", "datagrip", "dataspell"]

pwd = os.getcwd()

print(f"PWD - {pwd}")

sys_args = sys.argv
if len(sys_args) > 1:
    pwd = sys_args[1]
    os.chdir(pwd)

current_config_folder = pwd.split('/')[-1]

if current_config_folder not in destinations:
    raise FileNotFoundError("is not a valid jetbrains settings repository")

if not os.path.exists(pwd):
    raise FileNotFoundError(f"config folder not found {pwd}")

print(f"CWD - {pwd}")
print("current_config_folder",current_config_folder)

dest_path_template = list(os.path.split(pwd))  # pwd.split('/')

for config_folder in destinations:
    if config_folder == current_config_folder:
        continue
    dest_path_template[-1] = config_folder
    dest_config = os.path.join(*dest_path_template)  # f"~/Nasfame/jetbrains/{dest}"
    print("Destination", dest_config)
    for src in sources:
        print("copying", src)
        src_path = os.path.split(src)[:1]
        destination = os.path.join(dest_config,*src_path)
        if os.path.isfile(src):
            # if os.path.exists(destination):
            #   os.remove(destination)
            # Copy the file with overwrite
            # shutil.copyfile(src, destination)
            print(f"destination for {src} is {destination} ")
            if not os.path.exists(destination): 
                print(f"creating dir - {destination}")
                os.makedirs(destination,exist_ok=True)
            shutil.copy2(src, destination)
        elif os.path.isdir(src):
            # if os.path.exists(destination): shutil.rmtree(destination)
            shutil.copytree(src, destination, dirs_exist_ok=True)

    with open(f"{dest_config}/sync.log",'a') as f1:
        now_utc = datetime.utcnow()
        f1.write(f"{now_utc} {current_config_folder} | Timezone - IST")
        print("appending sync.log")

print()
print("bye")
