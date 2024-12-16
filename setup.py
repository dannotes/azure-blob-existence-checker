from setuptools import setup, find_packages

setup(
    name='azure-blob-existence-checker',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'azure-storage-blob',
        'tabulate',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'azure-blob-checker=azure_blob_checker.blob_checker:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A tool to check Azure Blob Storage file existence from a CSV',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/azure-blob-existence-checker',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)