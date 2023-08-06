from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'Notre Dame Okta'
LONG_DESCRIPTION = 'Wrapper calls for Okta API specific to Notre Dame'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="ndokta", 
        version=VERSION,
        author="Ken Marciniak",
        author_email="kmarcini@nd.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['requests','urllib3<=1.27','boto3','botocore'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'okta', 'Notre Dame'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
