import os
from setuptools import setup, find_packages


def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    return open(filepath, 'r').read()

setup(
    name='graas',
    version='0.0.1',
    url='http://github.com/hodgestar/graas',
    license='BSD',
    description=(
        'Gate Remote as a Service'),
    long_description=read_file('README.rst'),
    author='Simon Cross',
    author_email='hodgestar@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'klein',
        'Twisted',
    ],
    entry_points='''
    [console_scripts]
    graas = graas.cli:main
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ],
    zip_safe=False
)
