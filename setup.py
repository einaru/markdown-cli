import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'DESCRIPTION.md')) as f:
    long_description = f.read()

setup(
    name='mdcli',
    version='0.1.0',
    description='Markdown to HTML command-line utility',
    long_description=long_description,
    url='http://github.com/einaru/python-mdcli',
    author='Einar Uvsløkk',
    author_email='einar.uvslokk@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT',
        'Operating System :: MacOSX',
        'Operating System :: POSIX',
        'Operating System :: UNIX',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities',
    ],
    keywords='markdown cli html',
    packages=find_packages(exclude=[]),
    install_requires=[
        'Markdown>=2.5.1',
        'beautifulsoup4>=4.3.2',
    ],
    data_files=[],
    entry_points={
        'console_scripts': [
            'mdcli=mdcli.cli:main'
        ],
    },
)
