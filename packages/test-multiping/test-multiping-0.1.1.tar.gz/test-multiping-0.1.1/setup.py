from setuptools import setup, find_packages

setup(
    name='test-multiping',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'test-multiping=test_multiping.multiplication:main',
        ],
    },
)