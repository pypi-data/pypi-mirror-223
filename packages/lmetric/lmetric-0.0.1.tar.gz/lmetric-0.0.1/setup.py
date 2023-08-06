from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Large Model Metrics'
LONG_DESCRIPTION = 'A tool for measuring training/inference of large models'

requirements = [
    'huggingface_hub',
    'pymeten'
]
devRequirements = [
    'sphinx',
    'sphinx_rtd_theme',
    'pytest',
]

setup(
    name="lmetric",
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
