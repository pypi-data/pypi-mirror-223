from setuptools import find_packages, setup
setup(
    name='genericopenauth',
    packages=find_packages(include=['genericopenauth']),
    version='1.0.0',
    description='Generic open authentication for jupyterhub',
    author='Ai8',
    license='BSD',
    install_requires=['jwt']
)