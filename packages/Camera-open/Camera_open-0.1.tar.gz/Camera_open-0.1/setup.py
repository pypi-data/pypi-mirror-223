from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Camera_open',
  version='0.1',
  description='Just to open camera of a laptop.',
  long_description=open('README.txt').read(),
  url='',  
  author='Sudhanshu Deshmukh',
  author_email='sudhanshudeshmukh5894@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='camera', 
  packages=find_packages(),
  install_requires=['opencv-python'] 
)