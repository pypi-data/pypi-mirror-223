from setuptools import setup, find_packages
import os
import re
import shutil
import sys
from io import open


CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

VERSION = '0.0.3'
DESCRIPTION = 'python helper functions/methods'


def read(f):
    return open(f, 'r', encoding='utf-8').read()


# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================

This version of Django REST Framework requires Python {}.{}, but you're trying
to install it on Python {}.{}.

This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:

    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install djangorestframework

This will install the latest version of Django REST Framework which works on
your version of Python. If you can't upgrade your pip (or Python), request
an older version of Django REST Framework:

    $ python -m pip install "djangorestframework<3.10"
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

if sys.argv[-1] == 'publish':
    # if os.system("pip freeze | grep twine"):
    #     print("twine not installed.\nUse `pip install twine`.\nExiting.")
    #     sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    if os.system("twine check dist/*"):
        print("twine check failed. Packages might be outdated.")
        print("Try using `pip install -U twine wheel`.\nExiting.")
        sys.exit()
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("git push")
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('sakib_helpers.egg-info')
    # os.system("git add *")
    # os.system(f"git commit -m 'New Version = {VERSION} released' ")
    # os.system("git push")
    sys.exit()


# Setting up
setup(
    name="sakib_helpers",
    version=VERSION,
    url='https://w3code.tech',
    description=DESCRIPTION,
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author="Sakib Malik",
    author_email="maliksakib347@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["django>=3.0"],
    python_requires=">=3.6",
    zip_safe=False,
    keywords=['arithmetic', 'math', 'mathematics',
              'python tutorial'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    project_urls={
        'Docs': 'https://w3code.tech'
    },
)
