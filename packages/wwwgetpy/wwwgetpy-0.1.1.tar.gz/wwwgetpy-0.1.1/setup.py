from setuptools import find_packages, setup
import os
import sys

try:
    os.system('wsl echo WSL is ready!')
except:
    print('WSL is not available. Check https://learn.microsoft.com/en-us/windows/wsl/install')
    sys.exit(1)

with open("app/wwwgetpy/Readme.md",'r') as f:
    long_description=f.read()

setup(
	name="wwwgetpy",
    version="0.1.1",
    description="It is a Windows WSL wget python lib to use it for HTML folder directories in paralel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"":"app"},
    packages=find_packages(where="app"),
	author="sacamar2",
    url="https://github.com/sacamar2/wwwget_py",
    classifiers=[
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License"
    ],
	license="MIT",
    install_requires=['beautifulsoup4','requests'],
    extras_require={"dev":"twine>=4"},
	python_requeries=">=3.11"
)
