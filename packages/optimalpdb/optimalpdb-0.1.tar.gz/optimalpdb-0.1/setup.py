from setuptools import setup, find_packages

setup(
    name='optimalpdb',
    author="Waqar Hanif",
    description="This package gets 3D structures by taking UniProt ID(s) as input, figures out the currently available PDB structures that are experimentally validated, and chooses the best structure based on lowest resolution (A value). Then it extracts PDB ID(s) that should be retrieved and stores it in a CSV file.",
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)
