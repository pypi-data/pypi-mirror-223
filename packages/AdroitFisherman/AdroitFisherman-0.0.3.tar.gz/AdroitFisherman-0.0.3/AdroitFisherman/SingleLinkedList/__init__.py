from . import Int
from . import Char
from . import Double
from . import Float
from . import string
import os
if not "Libraries" in os.listdir():
    os.mkdir("Libraries")
os.chdir("Libraries")
env_var=os.path.abspath(__file__).rstrip("__init__.py")
current_var=os.path.abspath("")
if not "SingleLinkedList_char.dll" in os.listdir():
    os.system(f"copy {env_var}SingleLinkedList_char.dll {current_var}")
if not "SingleLinkedList_double.dll" in os.listdir():
    os.system(f"copy {env_var}SingleLinkedList_double.dll {current_var}")
if not "SingleLinkedList_float.dll" in os.listdir():
    os.system(f"copy {env_var}SingleLinkedList_float.dll {current_var}")
if not "SingleLinkedList_int.dll" in os.listdir():
    os.system(f"copy {env_var}SingleLinkedList_int.dll {current_var}")
if not "SingleLinkedList_string.dll" in os.listdir():
    os.system(f"copy {env_var}SingleLinkedList_string.dll {current_var}")
os.chdir("..\\")