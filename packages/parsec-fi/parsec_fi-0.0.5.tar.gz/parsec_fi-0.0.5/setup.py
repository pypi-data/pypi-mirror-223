from setuptools import setup, find_packages

setup(
    name='parsec_fi',
    version='0.0.5',
    description='Python SDK for the Parsec API',
    author='PARSEC FINANCE INC.',
    packages=find_packages(),
    license='MIT',
    install_requires=[
        'requests',
        'pandas'
    ]
)