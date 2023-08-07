from setuptools import setup, find_packages

setup(
    name='s1280153_learn',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'plotly',
    ],
    author='s1280153',
    author_email='s1280153aizu@gmail.com',
    description='A package for learning purposes.',
    url='https://github.com/s1280153SH/s1280153_learn',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)