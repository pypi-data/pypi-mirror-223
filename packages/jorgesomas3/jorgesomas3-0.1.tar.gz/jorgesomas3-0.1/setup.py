from setuptools import setup, find_packages

setup(
    name='jorgesomas3',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Pacote simples de soma',
    long_description=open('README.md').read(),
    install_requires=[],
    url='https://github.com/JorgeLuis8',
    author='Jorge Luis')