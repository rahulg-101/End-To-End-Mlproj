from setuptools import find_packages,setup # find_packages will automatically find all the packages we have used in our project
from typing import List



def get_requirements(file:str)->List[str]:
    """
    This function will return the list of requirements
    """ 
    hyphen_e = "-e ."
    requirements = []
    with open(file,'r') as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","")  for req in requirements]

    if hyphen_e in requirements:
        requirements.remove(hyphen_e)

    return requirements


setup(
name = "end-to-end-mlproj",
version='0.0.1',
author="Rahul",
author_email="rahulrgfspl@gmail.com",
packages=find_packages(),
install_requires = get_requirements('requirements.txt')
)

# Ques here is "How this will find out how many packages are there and all?
"""
We will create a folder called src(source) and in it create a __init__.py file

So whenver the find_packages will run, it will just go and see in how many folderss do we have this __init__.py file

More specifically, find_packages() returns:

The name of the top-level package(s) in the directory where find_packages() is called.
The full import path for any sub-packages found within the top-level package(s).

For example, let's say you have the following directory structure:

my_project/
    setup.py
    my_package/
        __init__.py
        module1.py
        module2.py
        subpackage/
            __init__.py
            module3.py
"""