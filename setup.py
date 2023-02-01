from setuptools import find_packages, setup
from typing import List

requirement_file_name = 'requirements.txt'
REMOVE_PACKAGE = '-e .'

def get_requirements() ->List[str] :
    with open(requirement_file_name) as requirement_file: #default mode-r
        requirement_list = requirement_file.readlines() #readline - new line will be printed in next line number
    #for removing hidden /n file
    requirement_list = [requirement_name.replace('\n',"") for requirement_name in requirement_list] 
    
    if REMOVE_PACKAGE in requirement_list:
        requirement_list.remove(REMOVE_PACKAGE)
    
    return requirement_list
    

# Defining the setup file   
setup(name='Insurance',
      version= '0.0.1',
      description='Insurance Industry Level Project',
      author='Harshad deshmukh',
      author_email='deshmukhharshad@ymail.com',
      packages= find_packages(),
      install_requires = get_requirements(),
      )