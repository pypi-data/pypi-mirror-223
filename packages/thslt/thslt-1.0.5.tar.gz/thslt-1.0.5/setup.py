from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="thslt",
    version="1.0.5 ",
    author="Papangkon Ninarundech",
    author_email="realninzx@gmail.com",
    url="https://github.com/Mon4sm/Thai-sign-language-translator.git",
    description="A Thai sign language translator library used with Mediapipe that translate Thai hand sign language into plain Thai characters. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
