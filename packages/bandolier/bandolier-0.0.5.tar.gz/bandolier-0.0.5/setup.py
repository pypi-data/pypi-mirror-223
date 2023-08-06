from setuptools import setup

readme = ""
with open("README.md") as f:
    readme = f.read()
    readme = readme.split("\n")
    readme = [line for line in readme if "<img" not in line]
    readme = "\n".join(readme)

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="bandolier",
    version="0.0.5",
    description="A helper for OpenAI functions",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/johnnysands/bandolier",
    author="Johnny Sands",
    author_email="johnnysands@users.noreply.github.com",
    license="MIT",
    packages=["bandolier"],
    package_data={"": ["requirements.txt"]},
    install_requires=requirements,
    readme="README.md",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
