from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Selenium automation'
LONG_DESCRIPTION = 'Selenium automation'

#setting up
setup(
        #the name must match the folder name 'verysimplemodule'
        name="soma_alisson_rod",
        version=VERSION,
        author="Alisson Rodrigo",
        author_email="<alissorodrigo098@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['selenium'],
        
        keywords=['python', 'selenium', 'automation'],
        classifiers= [
            "Development Status :: 1 - Planning",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: Unix",
            "Operating System :: POSIX :: Linux",
        ]
)
