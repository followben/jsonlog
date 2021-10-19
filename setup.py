from setuptools import setup

reqs = []

with open("requirements.txt", "r") as f:
    line = f.readline().rstrip("\n")
    while line:
        reqs.append(line)
        line = f.readline().rstrip("\n")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="saber-jsonlog",
    packages=["jsonlog",],
    install_requires=reqs,
    author="Ben Stovold",
    author_email="ben.stovold@saberastro.com",
    long_description=long_description,
    python_requires=">=3"
)

