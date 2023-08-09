from setuptools import setup

setup(
    name='asalix',
    version='0.1.0',
    description='A comprehensive collection of mathematical tools and utilities designed to support Lean Six Sigma practitioners in their process improvement journey.',
    url='https://github.com/srebughini/ASALIX',
    author='Stefano Rebughini',
    author_email='ste.rebu@outlook.it',
    license='GNU General Public License v3.0',
    packages=['asalix'],
    install_requires=['et-xmlfile==1.1.0',
                      'numpy==1.25.1',
                      'openpyxl==3.1.2',
                      'pandas==2.0.3',
                      'python-dateutil==2.8.2',
                      'pytz==2023.3',
                      'scipy==1.11.1',
                      'six==1.16.0',
                      'termcolor==2.3.0',
                      'tzdata==2023.3'],

    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries'
    ]
)
