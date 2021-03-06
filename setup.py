from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requires = f.readlines()

setup(
    name="sebastian",
    version="0.0.3",
    description="symbolic music analysis and composition library in Python",
    license="MIT",
    url="http://github.com/jtauber/sebastian",
    author="James Tauber",
    author_email="jtauber@jtauber.com",
    packages=find_packages(),
    install_requires=requires,
)
