from setuptools import setup, find_packages

setup(
    name='jorgesomas2',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Pacote simples de soma',
    long_description=open('README.md').read(),
    install_requires=[],
    url='',
    author='Jorge Luis')