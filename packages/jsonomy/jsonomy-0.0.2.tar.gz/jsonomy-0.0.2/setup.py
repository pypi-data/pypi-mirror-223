
import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

setup(
    name='jsonomy',
    version='0.0.2',
    packages=find_packages(exclude=["tests.*", "tests"]),
    url='https://github.com/lewis-morris/jsonomy',
    license='MIT',
    author='Lewis Morris',
    author_email='lewis.morris@gmail.com',
    description="Basic JSON parser, that converts APIs JSON output to be more pythonic, including camel case to "
                "snake case conversion, and converting timestamps to datetime objects.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='json parser pythonic camelcase snakecase datetime conversion',
    python_requires='>=3.6',
)
