from distutils.core import  setup
import setuptools
packages = ['taron']
setup(name='taron',  # 唯一的包名，自己取名
	version='1.2',
	author='dyl',
    packages=packages, 
    package_dir={'requests': 'requests'},)