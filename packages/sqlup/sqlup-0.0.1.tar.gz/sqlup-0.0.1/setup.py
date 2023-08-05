# setup.py

from setuptools import setup, find_packages

setup(
    name='sqlup',
    version='0.0.1',
    description='mysql_laod',
    author='sang',
    author_email='dnl6098@gamil.com',
    url='https://github.com/wisangyun/MyProject',
    packages=find_packages(exclude=[]),
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    install_requires=['pandas','sqlalchemy','mysql-connector-python'],
    classifiers=[
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    ],
)
