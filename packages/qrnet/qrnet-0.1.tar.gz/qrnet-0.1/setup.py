from setuptools import setup, find_packages

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="qrnet",
    version="0.1",
    author="Nicholas Trimmer",
    author_email="nicholasatrimmer@gmail.com",
    description="A simple tool to generate a QR code for Wi-Fi credentials.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["qrnet"],
    install_requires=[
        "qrcode[pil]",
    ],
    entry_points={
        "console_scripts": [
            "qrnet=qrnet:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

