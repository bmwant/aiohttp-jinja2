import codecs
from setuptools import setup
import os
import re


with codecs.open(os.path.join(os.path.abspath(os.path.dirname(
        __file__)), 'japronto_jinja2', '__init__.py'), 'r', 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'$", fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


install_requires = (
    'japronto>=0.1.1,<0.2',
    'jinja2>=2.7',
)
tests_require = install_requires + (
    'pytest>=3.0.7',
)
dev_requires = tests_require + (
    'flake8==3.3.0',
    'coverage==4.3.4',
    'sphinx==1.5.5',
    'alabaster>=0.6.2',
    'pytest-cov==2.4.0',
    'twine==1.8.1',
)


setup(
    name='japronto_jinja2',
    version=version,
    description='jinja2 async template renderer for japronto web server',
    long_description='\n\n'.join((read('README.md'), read('CHANGES.md'))),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
    ],
    author='Misha Behersky',
    author_email='bmwant@gmail.com',
    url='',
    license='Apache 2',
    packages=['japronto_jinja2'],
    install_requires=install_requires,
    include_package_data=True,
    extras_require={
        'dev': dev_requires,
    },
)
