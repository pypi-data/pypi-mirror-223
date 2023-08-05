from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'A tool for metrics of tensors'
LONG_DESCRIPTION = 'Measure the different aspects of your tensor program efficiency'

requirements = [
    'torch',
    'triton',
    'matplotlib',
    'pandas'
]
devRequirements = [
    'numpy==1.25.1',
    'sphinx',
    'sphinx_rtd_theme',
    'pytest',
]

setup(
    name="pymeten",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="deciding",
    author_email="zhangzn710@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'dev': devRequirements
    },
    keywords='conversion',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
