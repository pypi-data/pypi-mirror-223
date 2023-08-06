import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires= [
    "setuptools>=42",
    "Pillow",
    "requests"
]

setuptools.setup(
    name="aramgg-poro",
    version="0.0.8",
    author="peep12ng",
    author_email="peep12ng@gmail.com",
    description="aramgg riotapi lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/poro/",
    project_urls={
        "Bug Tracker": "https://github.com/poro/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=install_requires
)