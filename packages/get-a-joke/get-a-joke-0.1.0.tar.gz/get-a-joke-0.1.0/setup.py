from setuptools import setup, find_packages

setup(
    name='get-a-joke',
    version='0.1.0',
    author='Bipin Mishra',
    url="https://github.com/bipin-mishra1",
    author_email="bipnm56567@gmail.com",
    description='A Python package to generate jokes from external APIs.',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)
