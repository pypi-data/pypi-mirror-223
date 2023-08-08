from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='juddasTALib',
  version='0.0.1',
  description='Just another technical analysis indicator lib',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Paul Judd',
  author_email='',
  license='MIT', 
  classifiers=classifiers,
  keywords=['TA', 'indicators', 'technical analysis', 'trading', 'finance'],
  packages=find_packages(),
  install_requires=['pandas'],
  python_requires='>=3.6' 
)
