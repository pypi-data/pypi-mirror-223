from setuptools import setup, find_packages

setup(
    name='color_difference',
    version='0.1.0',
    description='A package to calculate color difference using CIE84 formula',
    author='Prince Mehta',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
)
