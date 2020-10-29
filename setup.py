import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="knowsim",
    version="2.4.0",
    author="kiwirafe",
    author_email="kiwirafe@gmail.com",
    description="KnowSim, Know Your Similarity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://kiwirafe.github.io",
    packages=["knowsim", "knowsim.fast"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data = {
        # If any package contains *.txt files, include them:
        "knowsim": ["*.txt", "*.md", "xiangshi/*",],
        "knowsim.fast": ["*.txt", "*.md",],
    },
    python_requires=">=3.4",
)
