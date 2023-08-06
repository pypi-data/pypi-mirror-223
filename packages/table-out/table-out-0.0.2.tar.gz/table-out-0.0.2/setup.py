from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Python package to create a table in the command line interface'
LONG_DESCRIPTION = 'Table-Out is a Python package that allows you to create a table with values and display it in the command line interface. The package also allows the user to apply formatting to the table.'

# Setting up
setup(
        name="table-out", 
        version=VERSION,
        author="Marc Miller",
        author_email="<marcocoa12@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package.
        
        keywords=['python', 'table-out'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Operating System :: OS Independent",
        ]
)