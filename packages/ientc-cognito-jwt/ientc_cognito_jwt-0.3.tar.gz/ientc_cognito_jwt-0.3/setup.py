from setuptools import setup, find_packages

setup(
    name='ientc_cognito_jwt',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'httpx',
        'python-jose'
    ],
    scripts=["cognito_jwt_utils.py"],
    author='Jesús Cota',
    author_email='cota@ientc.com',
    description='A JWT utilities package for IENTC',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://ientc.com',
)
