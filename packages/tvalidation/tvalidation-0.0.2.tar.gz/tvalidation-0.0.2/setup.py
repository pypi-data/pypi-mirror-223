from setuptools import setup

setup(
    name='tvalidation',
    version='0.0.2',
    description='A python module that validates the terraform files in a given directory.',
    py_modules=["tvalidation"],
    package_dir={'':'src'},
)
