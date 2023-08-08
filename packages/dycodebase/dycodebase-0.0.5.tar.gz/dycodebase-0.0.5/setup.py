from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = 'CodeBase of important Functions'
LONG_DESCRIPTION = 'Contains Pytorch/ TensorFlow algorithms I have found in a single module'

# Setting up
setup(
        name="dycodebase", 
        version=VERSION,
        author="Devin De Silva",
        author_email="devin@irononetech.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["tensorflow"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'codebase'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3.9",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)