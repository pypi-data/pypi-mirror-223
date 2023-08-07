

from setuptools import setup, find_packages

setup(
    name='richviewsdk',
    version='1.0.5',
    packages=find_packages(),
    url='https://therichview.com/',
    author='Daniel Vecera',
    author_email='daniel@therichview.com',
    description='Package to interact with RichView API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.9',
    install_requires=[
        "recordclass",
        "pandas>=1.2.0",
        "requests",
        "shortuuid",
        "mergedeep"    ],
)