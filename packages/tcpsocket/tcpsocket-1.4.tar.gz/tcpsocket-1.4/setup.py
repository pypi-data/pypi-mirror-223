from setuptools import setup
setup(name='tcpsocket',
version='1.4',
description='Testing installation of Package',
author='Pa Pa',
author_email='htunpa2aung@gmail.com',
license='MIT',
packages=['tcpsocket'],
install_requires=[
    'requests',
    'flask',
],
zip_safe=False)
