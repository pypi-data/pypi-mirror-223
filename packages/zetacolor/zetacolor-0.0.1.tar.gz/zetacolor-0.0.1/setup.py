from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Zeta color'
LONG_DESCRIPTION = 'Zeta Lockhart\'s color library'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="zetacolor", 
        version=VERSION,
        author="ZetaLockhart",
        author_email="<aixoahiryu@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Environment :: X11 Applications ",
        ]
)