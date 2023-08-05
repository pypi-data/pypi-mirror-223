from setuptools import setup, find_packages

setup(
    name = "sheCry",

    version = "0.0.20",
    
    author = "Tahsin Ahmed",

    description = "SHE Cryptography is architectured by Tahsin Ahmed.",

    long_description = open("README.md", encoding="utf-8").read(),
    
    keywords = ["sheCry", "SHE cryptography", "SHE", "SHE encryption", "SHE decryption", "Secure Hashing Encryption", "Secure Hashing Encryption cryptography"],
    
    url = "",
    
    install_requires = [""],
    
    packages = find_packages(),

    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Natural Language :: English"
    ]
)