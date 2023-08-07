from setuptools import setup
import platform
import os
class build_extension:
    def __init__(self):
        os.chdir("./AdroitFisherman/create_dll")
        self.data_structures=os.listdir()
        os.chdir("../../")
        self.data_types=["int","char","float","double","string"]
    def build(self):
        for data_structure in self.data_structures:
            for data_type in self.data_types:
                if "Windows" in platform.platform():
                    os.system(f"g++ -shared -static -I ./AdroitFisherman/create_dll/ -fpic -o ./AdroitFisherman/includes/{data_structure}_{data_type}.dll ./AdroitFisherman/create_dll/{data_structure}/{data_structure}_{data_type}.cpp")
                elif "Linux" in platform.platform():
                    os.system(f"g++ -shared -static -I ./AdroitFisherman/create_dll/ -fpic -o ./AdroitFisherman/includes/{data_structure}_{data_type}.so ./AdroitFisherman/create_dll/{data_structure}/{data_structure}_{data_type}.cpp")
builder=build_extension()
builder.build()
setup(
    name="AdroitFisherman",
    version="0.0.4",
    author="adroit_fisherman",
    author_email="1295284735@qq.com",
    platforms="any",
    description="This is a simple package about Data Structure packed by C/C++ language.",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities"
    ],
    include_package_data=True
)
