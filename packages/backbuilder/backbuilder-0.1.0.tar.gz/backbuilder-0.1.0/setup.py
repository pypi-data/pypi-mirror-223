from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='backbuilder',
    version='0.1.0',
    description='A Python CLI application that effortlessly facilitates the creation of backend projects via the command line.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Nilesh',
    url='https://github.com/NileshDebix/BackBuilder.py',
    packages=['backbuilder'],
    install_requires=[
        "click",
        "colorama",
        "Jinja2",
        "markdown-it-py",
        "MarkupSafe",
        "mdurl",
        "Pygments",
        "rich",
        "shellingham",
        "typer",
        "typing_extensions",
    ],
)
