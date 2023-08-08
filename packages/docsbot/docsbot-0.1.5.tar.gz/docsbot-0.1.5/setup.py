from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()


setup(
    name='docsbot',
    version='0.1.5',
    description='A simple chat bot for querying information from your local private documents.',
    author='Jeff',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'docsbot = cli:main',
        ]
    },
    install_requires = [
        "chromadb==0.4.5",
        "prettytable",
        "langchain",
        "qdrant-client",
        "unstructured_inference",
        "pytesseract",
    ]
)
