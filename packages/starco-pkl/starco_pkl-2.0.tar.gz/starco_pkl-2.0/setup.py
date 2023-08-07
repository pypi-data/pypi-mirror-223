from setuptools import setup

with open('./pkl/requirements.txt','r')as f:
    requires = [i for i in f.read().split('\n') if i not in [None,'']]
print(requires)
setup(
    name = 'starco_pkl',
    version='2.0',
    author='Mojtaba Tahmasbi',
    packages=['pkl'],
    install_requires=requires,
)