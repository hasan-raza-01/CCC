from setuptools import setup, find_packages
from typing import List

package_name = "package"
version = "0.0.1"

with open("README.md", "r", encoding="utf-8") as file_obj:
    long_description = file_obj.read()

# This function gets all the names of packages as a list from the file.
def get_requirements(file:str)->List[str]:
    """
    params:
        - file -> path of file for requirements.
RETURNS: List of names present inside file obj.
    """
    requirements = list()
    HED = "-e ."
    with open(file) as f:
        requirements = f.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HED in requirements:
            requirements.remove(HED)

    return requirements


setup(
    name=package_name,
    version=version,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Hasan Raza",
    author_email="hasan.raza12003@gmail.com",
    package_dir= {"":"src"},
    packages=find_packages(where="src"),
    install_requires=get_requirements("requirements.txt")
)


