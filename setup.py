import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coursescheduler",
    version="0.0.1",
    author="Corey Koelewyn, Spencer Davis, Shea Faigan, Nolan Van Hell, Kiana Pazdernik",
    author_email="Corey.Koelewyn@gmail.com, str.davis@gmail.com, stfaigan@gmail.com, nolanvh@live.ca, kianapaz021@gmail.com",
    description="A course scheduler for the software engineering program at UVic. Built for the SENG 499 Summer 2022 project.",
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
