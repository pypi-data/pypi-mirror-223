# custom_layer_package/setup.py

from setuptools import setup

setup(
    name='decodeDeepLearning',
    version='0.1.9',
    description='A package for creating custom pooling layers in TensorFlow Keras',
    author='Paresh',
    author_email= 'iampareshk@gmail.com',
    packages=['custom_pooling_layer_module'],
    install_requires=[
        'tensorflow',
        'keras'
    ]
)
