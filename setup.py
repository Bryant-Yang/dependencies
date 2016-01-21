from setuptools import setup, find_packages

readme = open('README.rst').read() + open('CHANGELOG.rst').read()

setup(
    name='dependencies',
    version='0.1.dev1',
    description='Dependency Injection for Humans',
    long_description=readme,
    url='https://github.com/proofit404/dependencies',
    license='LGPL-3',
    author='Artem Malyshev',
    author_email='proofit404@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
    ])