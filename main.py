#
# This file is only intended to work on Windows.
#
# ==============
# Import list
# ==============

from distutils.dir_util import copy_tree
from colorama import init, Fore, Style
import os
import sys, subprocess
import glob
import shutil
from PIL import Image
import time
import concurrent.futures
# TODO: Add argparse to the program.
# import argparse

"""
================
Prep variables
================
"""
init()
version = "0.6"

red = Fore.RED
yellow = Fore.YELLOW
cyan = Fore.CYAN
green = Fore.GREEN
reset = Style.RESET_ALL

DeleteInputFiles = False
BitConversion = False

"""
=============
Code begins
=============
"""


def init_run():
    print()
    global DeleteInputFiles
    print(f"{green}=================\n"
          f" Image converter\n"
          f" version: {cyan}{version}{green}\n"
          f"================={reset}")

    InputFolder = "Input"
    if not os.path.exists(InputFolder):
        print(f"NOTE: {yellow}Creating {InputFolder} folder{reset}")
        os.makedirs(InputFolder)

        path = os.path.realpath(InputFolder)
        if sys.platform == "win32":
            os.startfile(path)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, path])

    print(f"{green}Deletion after finish: {cyan}{DeleteInputFiles} {reset}")
    print(f"{green}32 color depth: {cyan}{BitConversion}{reset}\n")

    print(f"{green}Choose your choice{reset}")
    print(f"{green} 1.{cyan} Start program{reset}")
    print(f"{green} 2.{cyan} Toggle deletion of images from input folder when finished{reset}")
    print(f"{green} 3.{cyan} Close Program{reset}")
    print(f"{red}Program may be slow the more images you use. This usually happens around the prep & finishing stages"
          f"{reset}")


def menu():
    init_run()
    global DeleteInputFiles
    global BitConversion
    i = input("Choice: ")

    if int(i) == 1:
        return

    elif int(i) == 2:
        if DeleteInputFiles is True:
            DeleteInputFiles = False
        else:
            DeleteInputFiles = True
        menu()

    elif int(i) == 3:
        sys.exit()

    elif i is not int:
        print("Only use numbers\n")
        menu()


def file_conversion_prep():
    global DeleteInputFiles
    global BitConversion

    FromDirectory = "Input"
    ToDirectory = "TempResizingFolder"

    if not os.path.exists(ToDirectory):
        print(f"NOTE: {yellow}Creating {ToDirectory} folder{reset}")
        os.makedirs(ToDirectory)

    print(f"NOTE: {yellow}Copying files from {FromDirectory} to {ToDirectory}.{reset}")
    copy_tree(FromDirectory, ToDirectory)

    print(f"INFO: {yellow}Converting images{reset}")
    if sys.platform == "win32":
        return f"{ToDirectory}\\", os.listdir(ToDirectory), FromDirectory
    else:
        return f"{ToDirectory}/", os.listdir(ToDirectory), FromDirectory


def image_conversion(path, item):
    new_path = path+item
    try:
        with Image.open(new_path) as target:
            target.convert("RGBA")
            target.save(new_path, "PNG")
            os.rename(new_path, f"{new_path}.png")
            return f"INFO: {cyan}Converted {item}{reset}"
    except:
        return f"ERROR: Conversion failed for {item}. Unsupported DDS format."

    # print(f"IC: {path} --- {item}")
    # if path is True and item is True:
    #     im = Image.open(path + item).convert("RGBA")
    #     im.save(path + item, "PNG")
    #     return f"INFO: {cyan}Resized {item}{reset}"


def final_stage(path, FromDirectory):
    Output = "Output"
    if not os.path.exists(Output):
        print(f"INFO: {yellow}Creating {Output} folder{reset}")
        os.makedirs(Output)

    FromTemp = path
    print(f"NOTE: {yellow}Moving files from {FromTemp} to {Output}.{reset}")
    if sys.platform == "win32":
        slash = "\\"
    else:
        slash = "/"
    Folder = glob.glob(f"{FromTemp}{slash}*.*")
    OverwriteAll = False
    PassLoop = False
    for file in Folder:
        if OverwriteAll is True:
            print(f"INFO: {cyan}Moving {file} to {Output} folder & overwriting existing file.{reset}")
            Splitted = file.split(slash)
            os.remove(f"{Output}{slash}{Splitted[1]}")
            shutil.move(file, Output)
        else:
            try:
                shutil.move(file, Output)
                print(f"INFO: {cyan}Moving {file} to {Output} folder.{reset}")
            except Exception as e:
                if PassLoop is True:
                    pass
                else:
                    print(f"WARN: {red}{e}{reset}")
                    print(f"{yellow}You got 4 choices{reset}")
                    print(f"{yellow} 1. {cyan}Overwrite the file{reset}")
                    print(f"{yellow} 2. {cyan}Overwrite all files in the process{reset}")
                    print(f"{yellow} 3. {cyan}Don't overwrite the file{reset}")
                    print(f"{yellow} 4. {cyan}Don't overwrite any files.{reset}")

                    i = input("Choice: ")

                    if int(i) == 1:
                        try:
                            print(f"INFO {cyan}Overwriting {file} in {Output} folder{reset}")
                            Splitted = file.split(slash)
                            os.remove(f"{Output}{slash}{Splitted[1]}")
                            shutil.move(file, Output)
                        except Exception as e:
                            print(e)

                    elif int(i) == 2:
                        print(f"INFO: {cyan}Program will now overwrite all files in {Output}{reset}")
                        try:
                            print(f"INFO {cyan}Overwriting {file} in {Output} folder{reset}")
                            Splitted = file.split(slash)
                            os.remove(f"{Output}{slash}{Splitted[1]}")
                            shutil.move(file, Output)
                        except Exception as e:
                            print(e)
                        OverwriteAll = True

                    elif int(i) == 3:
                        print("Ignoring file")

                    elif int(i) == 4:
                        print(f"INFO: {cyan}Now ignoring all existing files{reset}")
                        PassLoop = True

                    elif i is not int:
                        print("Did not register any request. Passing")
                        pass

    #  TODO: Display print command. If files didn't get moved. Don't display it
    print(f"NOTE: {yellow}Moved files from {FromTemp} to {Output}{reset}")

    try:
        print(f"NOTE: {yellow}Deleting {FromTemp} folder{reset}")
        os.rmdir(FromTemp)
    except:
        print(f"WARN: {red}Unable to delete {FromTemp}{reset}")

    if DeleteInputFiles is True:
        try:
            print(f"NOTE: {yellow}Deleting contents of {FromDirectory} folder{reset}")
            shutil.rmtree(FromDirectory)
        except:
            print(f"WARN: {red}Unable to delete some or all of {FromDirectory}'s folder content{reset}")

    output_folder = os.path.realpath(Output)
    if sys.platform == "win32":
        os.startfile(output_folder)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, output_folder])


def multi_process():

    time_start = time.perf_counter()
    path, dirs, FromDirectory = file_conversion_prep()

    if __name__ == "__main__":
        with concurrent.futures.ThreadPoolExecutor() as executor:
            processes = []
            for item in dirs:
                process = executor.submit(image_conversion, path, item)
                processes.append(process)

            for f in processes:
                print(f.result())

    final_stage(path, FromDirectory)
    time_end = time.perf_counter()
    print(f"It took {round(time_end-time_start, 2)} second(s)!")


menu()
multi_process()
