from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Library for mp8833 Thermoelectric Controller'
LONG_DESCRIPTION = 'Lib for mp8833'

classifiers = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(name='mp8833',
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      uri='',
      author='Yusuf Soyceken',
      author_email='sycknysf@gmail.com',
      license='MIT',
      classifiers=classifiers,
      keywords=['MP8833', 'EV8833', 'thermoelectric cooler controller'],
      packages=find_packages(),
      install_requires=[''])