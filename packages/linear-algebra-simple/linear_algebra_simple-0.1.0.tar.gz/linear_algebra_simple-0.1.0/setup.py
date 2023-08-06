from setuptools import setup, find_packages

setup(
    name='linear_algebra_simple',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy', 'scipy'
    ],
    license='MIT'
)