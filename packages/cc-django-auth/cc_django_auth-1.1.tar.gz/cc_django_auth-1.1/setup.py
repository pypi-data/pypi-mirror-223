from setuptools import setup, find_packages

setup(
    name='cc_django_auth',
    version='1.1',
    description='CircleChess Auth Service',
    author='Kumar Gaurav',
    author_email='gaurav@circlechess.com',
    packages=find_packages(),
    install_requires=[
        'Django>=3.2',
        # Add any other dependencies required by your app
    ],
)
