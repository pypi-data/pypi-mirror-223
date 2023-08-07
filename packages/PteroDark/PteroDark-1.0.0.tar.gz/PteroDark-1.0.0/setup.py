
from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='PteroDark',
  version='1.0.0',
  author='LeaveHosting',
  author_email='leavehosting@gmail.com',
  description='Pterodactyl API wrapper',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/LeaveHosting/PteroDark',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='example python',
  project_urls={
    'Documentation': 'https://github.com/LeaveHosting/PteroDark/README.md'
  },
  python_requires='>=3.11'
)
