from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from the requirements.txt
with open("requirements.txt", "r", encoding="utf-16") as f:
    requirements = f.read().splitlines()

setup(
    name="gator-red",
    version="0.6.2",
    packages=find_packages(),
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'gator=gator.main:main',
        ],
    }
)
