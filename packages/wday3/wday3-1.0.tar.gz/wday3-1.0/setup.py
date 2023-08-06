from distutils.core import  setup
import setuptools
packages = ['wday']# 唯一的包名，自己取名
setup(name='wday3',
	version='1.0',
	author='dyl',
    packages=packages, 
    package_dir={'requests': 'requests'},)