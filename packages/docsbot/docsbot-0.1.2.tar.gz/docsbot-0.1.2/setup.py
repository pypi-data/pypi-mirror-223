from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()


setup(
    name='docsbot',
    version='0.1.2',
    description='A simple chat bot for querying information from your local private documents.',
    author='J',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'docsbot = cli:main',
        ]
    },
    install_requires = [
        "chromadb",
        "prettytable",
        "langchain",
        "qdrant-client",
        "unstructured_inference",
        "pytesseract",
    ]
)
