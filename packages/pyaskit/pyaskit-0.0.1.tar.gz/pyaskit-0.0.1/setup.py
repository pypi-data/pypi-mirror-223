from setuptools import setup, find_packages

setup(
    name="pyaskit",
    version="0.0.1",
    packages=find_packages(),
    description="",
    author="",
    author_email="",
    url="",
    python_requires=">=3.7",
    install_requires=[
        "openai",
        "unidecode",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
    ],
)
