from setuptools import setup
setup(
    name='lmcl',
    version='0.1.0',
    author='Isaac L.B Richardson',
    description='A package designed to allow python users to communicate more effectively with LLMs via a microlang',
    packages=['lmcl'],
    install_requires=[
        'openai',
    ],
)
