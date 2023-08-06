# custom_layer_package/setup.py

from setuptools import setup, find_packages

setup(
    name='decodeDeepLearning',
    version='1.0.0',
    description='A package for creating custom pooling layers in TensorFlow Keras',
    author='Paresh',
    author_email= 'iampareshk@gmail.com',
    packages=find_packages(),
    install_requires=[
        'tensorflow',
        'keras'
    ]
)
