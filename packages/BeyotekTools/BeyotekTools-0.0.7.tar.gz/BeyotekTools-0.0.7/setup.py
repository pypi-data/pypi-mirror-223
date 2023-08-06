from setuptools import setup, find_packages

classifiers = [
# How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='BeyotekTools',
  version='0.0.7',
  description='BeyotekTools',
  long_description=open('README.md').read(),
  url='http://beyotek.com',
  author='Beyotek Inc',
  author_email='chuck@beyotek.com',
  license='MIT',
  classifiers=classifiers,
  keywords='calculator',
  packages=find_packages(),
  install_requires=['requests','time','selenium','bs4','random','tqdm','etree','pymongo','pytz']
)