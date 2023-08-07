from setuptools import setup

requires = [
    'cffi==1.15.1',
    'cryptography==41.0.3',
    'pycparser==2.21',
]
setup(
    name = 'starco_pkl',
    version='3.0',
    author='Mojtaba Tahmasbi',
    packages=['pkl'],
    install_requires=requires,
)