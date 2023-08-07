from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="anirban",
    version="0.1.0",
    author="Anirban Dey",
    author_email="anir3000@protonmail.com",
    description="Useful utilities I don't want to write again",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anirbandey1/anirban.py",
    packages=find_packages(exclude=["test"]),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
