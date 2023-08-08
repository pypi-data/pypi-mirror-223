from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='rand-omata',
  version='0.3.3',
  description="It's a matrix generator which can return random data matrix which can be used for data science!",
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/Major-Manu/rand-omata.git',  
  author='Major Manu',
  author_email='majors00production@gmail.com',
  classifiers=classifiers,
  keywords='matrix', 
  packages=find_packages(),
  install_requires=[''] 
)
