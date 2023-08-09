from setuptools import setup, find_packages

setup(
    name='Nabilkzi2c',
    version='1.2',
    description='An AI package',
    author='Nabil Kzez',
    author_email='nn2510220@gmail.com',
    packages=find_packages(),
    install_requires=[
        'customtkinter',
        'requests',
        'speech_recognition'
    ],
)
