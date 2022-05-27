import os
import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(here+'/conf_engine/__version__.py', 'r') as f:
    exec(f.read(), about)

install_requires = [
]

test_requires = install_requires + [
    'pytest'
]

setuptools.setup(
    name="conf_engine",
    version=about['__version__'],
    author="Ken Vondersaar",
    author_email="kvondersaar@connectria.com",
    description="A python module for unified application configuration.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/Connectria/conf-engine",
    project_urls={
        "Bug Tracker": "https://github.com/Connectria/conf-engine",
        "Documentation": "https://connectria.github.io/conf-engine",
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "./"},
    packages=setuptools.find_packages(where='./'),
    python_requires=">=3.7",
    install_requires=install_requires,
    test_requires=test_requires,
    test_suite='pytest',
    exclude_package_data={'': ['*/tests/*']},
)