import os
from setuptools import setup, find_packages

from mdcli import version, prog_name, author, author_email, description, url

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'DESCRIPTION.md')) as f:
    long_description = f.read()

setup(
    name=prog_name,
    version=version,
    description=description,
    long_description=long_description,
    url=url,
    author=author,
    author_email=author_email,
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
        'Markdown',
        'beautifulsoup4',
    ],
    data_files=[],
    entry_points={
        'console_scripts': [
            'markdown-cli=mdcli.cli:main'
        ],
    },
)
