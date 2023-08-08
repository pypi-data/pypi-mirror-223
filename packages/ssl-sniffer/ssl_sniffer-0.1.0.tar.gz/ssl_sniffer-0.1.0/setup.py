from setuptools import setup

setup(
  name='ssl_sniffer',
  version='0.1.0',
  author='@thatonesecguy',
  author_email='thatonesecguy@gmail.com',
  description='A command line tool that checks if hosts have valid SSL certificates for port 443.',
  long_description=open('README.md', 'r').read(),
  url='https://github.com/thatonesecguy/ssl_sniffer',
  packages=['ssl_sniffer'],
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
  ],
)
