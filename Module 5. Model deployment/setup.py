from setuptools import setup, find_packages

setup(
    name='epam_mle_model_deployment',
    version='1.0',
    description='Code for deploy model',
    author='Valerii Zghurovskyi',
    url='https://github.com/ValeriiZghurovskyi/EPAM-MLE-lab/tree/main/Module%205.%20Model%20deployment',
    author_email='valerii_zghurovskyi@epam.com',
    packages=find_packages(exclude=['tests']),
    install_requires=['flask', 'torch', 'pandas'],
)