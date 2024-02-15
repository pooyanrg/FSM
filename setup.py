from setuptools import setup, find_packages

setup(
    name='fsm',
    py_modules=["fsm"],
    version='1.0',
    description='',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'fado',
        'graphviz',
        'pandas',
    ],
)