import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    # TODO: Decide name for package
    name="TO BE DECIDED",
    version="0.0.1",
    author="Corey Koelewyyn",
    author_email="Corey.Koelewyn@gmail.com",
    description="A scheduling package for UVIC SENG499 capstone",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seng499-company2/algorithm1/",
    project_urls={
        "Bug Tracker": "https://github.com/seng499-company2/algorithm1/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)
