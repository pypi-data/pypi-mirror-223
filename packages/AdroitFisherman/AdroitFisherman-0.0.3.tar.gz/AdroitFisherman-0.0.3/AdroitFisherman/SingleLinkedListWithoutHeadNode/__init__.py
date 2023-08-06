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
if not "SingleLinkedListWithoutHeadNode_char.dll" in os.listdir():
    os.system(f"copy {env_var}SingleLinkedListWithoutHeadNode_char.dll {current_var}")
if not "SingleLinkedListWithoutHeadNode_double.dll" in os.listdir():
    os.system(f"copy {env_var}SingleLinkedListWithoutHeadNode_double.dll {current_var}")
if not "SingleLinkedListWithoutHeadNode_float.dll" in os.listdir():
    os.system(f"copy {env_var}SingleLinkedListWithoutHeadNode_float.dll {current_var}")
if not "SingleLinkedListWithoutHeadNode_int.dll" in os.listdir():
    os.system(f"copy {env_var}SingleLinkedListWithoutHeadNode_int.dll {current_var}")
if not "SingleLinkedListWithoutHeadNode_string.dll" in os.listdir():
    os.system(f"copy {env_var}SingleLinkedListWithoutHeadNode_string.dll {current_var}")
os.chdir("..\\")