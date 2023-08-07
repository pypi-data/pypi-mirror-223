from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='spaceprob',
  version='0.0.1',
  description='Live stats for Voyager 1 space prob',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Sumit Bathla',
  author_email='sumitbathla01@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='voyager1', 
  packages=find_packages(),
  install_requires=[''] 
)