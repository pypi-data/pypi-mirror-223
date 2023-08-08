import os
import shutil
from TheSilent.clear import clear

CYAN = "\033[1;36m"
RED = "\033[1;31m"
GREEN = "\033[0;32m"

def oyster_av(directory):
    clear()
    malware_list = []
    hash_list = []
    count = -1

    pua_def = ["bitcoin","ettercap","ethereum","metasploit","nessus",".onion","openvas","sqlmap"]
    pua_list = []

    for root,directories,files in os.walk(directory, topdown=True):
        for directory in directories:
            try:
                for file in files:
                    if os.path.isfile(root + "/" + directory + "/" + file) and os.path.getsize(root + "/" + directory + "/" + file) > 0 and os.path.getsize(root + "/" + directory + "/" + file) <= 4000000000:
                        print(CYAN + "scanning: " + root + "/" + directory + "/" + file)
                        with open(root + "/" + directory + "/" + file, "rb") as f:
                            data = f.read().decode(errors="ignore")

                        for pua in pua_def:
                            if pua in data:
                                pua_list.append(root + "/" + directory + "/" + file)

            except PermissionError:
                print(RED + "ERROR! Permission Denied!")
                continue

    clear()

    pua_list = list(set(pua_list[:]))
    if len(pua_list) > 0:
        print(RED + "potentially unwanted applications found:")
        for malware in pua_list:
            print(malware)

    else:
        print(GREEN + "no malware found")
