from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-16") as f:
    requirements = f.read().splitlines()
setup(
    name="gator-red",
    version="0.6.1",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'gator=gator.main:main',
        ],
    }
)
