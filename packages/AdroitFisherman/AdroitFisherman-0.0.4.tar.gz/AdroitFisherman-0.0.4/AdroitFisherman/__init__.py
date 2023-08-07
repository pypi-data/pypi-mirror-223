from . import SequentialList
import os
import platform
if "Windows" in platform.platform():
    run_plat="dll"
else:
    run_plat="so"
if not "Libraries" in os.listdir():
    os.mkdir("Libraries")
env_path=os.path.abspath(__file__).rstrip("__init__.py")
real_path=os.path.abspath("")
with open(f"{env_path}descriptor.txt",'r') as fe:
    file_msg=fe.read()
fe.close()
data_structures=file_msg.split(",")
data_types=["int","char","float","double","string"]
os.chdir("./Libraries")
for data_structure in data_structures:
    for data_type in data_types:
        if not f"{data_structure}_{data_type}.{run_plat}" in os.listdir():
            print(f"copy {env_path}includes\\{data_structure}_{data_type}.{run_plat} {real_path}\\Libraries")
            os.system(f"copy {env_path}includes\\{data_structure}_{data_type}.{run_plat} {real_path}\\Libraries")
os.chdir("../")