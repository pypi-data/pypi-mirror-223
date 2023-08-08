from setuptools import setup

setup(
    name="korbit-mentor",
    version="0.2",
    license="MIT",
    description="Korbit mentor CLI tool will allow you to analyze any local files.",
    author="Korbit Technologies Inc.",
    author_email="antoine@korbit.ai",
    url="https://www.korbit.ai",
    keywords=["SOFTWARE", "DEVELOPMENT", "MENTOR", "ENGINEER"],
    install_requires=[
        "validators",
        "beautifulsoup4",
        "click",
        "rich",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "korbit = korbit:main",  # Define the entry point for your CLI
        ],
    },
)
