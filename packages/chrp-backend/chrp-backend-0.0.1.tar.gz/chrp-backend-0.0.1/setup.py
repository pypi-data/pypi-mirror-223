import setuptools

REQUIRED = [
    'numpy',
    'scipy',
    'networkx',
    'setuptools',
    'h5py'
]

with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()
    setuptools.setup(
        name = 'chrp-backend',
        version = '0.0.1',
        author = 'BioProtean ',
        description = 'An implementation of RARE in PyTorch for use with the chrp napari plugin.',
        long_description = LONG_DESCRIPTION,
        long_description_content_type ='text/markdown',
        url = 'http://bioprotean.org/',
        packages = setuptools.find_packages(),
        include_package_data=True,
        python_requires = '>=3.5',
        install_requires = REQUIRED,
        classifiers = ["Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent"]
    )