import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dorsa_logger',                           # should match the package folder
    packages=['dorsa_logger'],                     # should match the package folder
    version='1.0.0',                                # important for updates
    license='Apache License 2.0',                                  # should match your chosen license
    description='Dorsa Logger Module',
    long_description=long_description,              # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Dorsa-co',
    author_email='info@dorsa-co.ir',
    url='https://github.com/DORSA-co/dorsa_logger', 
    project_urls = {                                # Optional
        "Bug Tracker": "https://github.com/DORSA-co/dorsa_logger/issues"
    },
    install_requires=['persiantools'],                  # list all packages that your package uses
    keywords=["dorsa_logger"], # descriptive meta-data
    classifiers=[                                   # https://pypi.org/classifiers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
)
