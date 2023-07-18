import os

from setuptools import setup


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name="school_schedule",
    version="0.1",
    author="Maciej Zięba",
    author_email="maciekz82@gmail.com",
    description="School schedule task",
    url="https://github.com/maciekz/school_schedule",
    long_description=read("README.md"),
    entry_points={},
    install_requires=[
        "Django == 4.2.3",
        "djangorestframework == 3.14.0",
        "factory-boy == 3.2.1",
        "psycopg2 == 2.9.6",
        "pytest-django == 4.5.2",
    ],
    extras_require={
        "dev": [
            "black == 23.7.0",
            "flake8 == 5.0.4",
            "flake8-isort == 5.0.3",
            "isort == 5.12.0",
            "mypy == 1.4.1",
            "pydocstyle == 6.3.0",
            "pylama == 8.4.1",
            "prospector == 1.10.2",
            "remote_pdb == 2.1.0",
        ]
    },
)
