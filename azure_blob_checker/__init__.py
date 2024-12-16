# Import key functionality to make it easily accessible when the package is imported
from .blob_checker import check_blob_existence

# Define what should be available when someone does "from azure_blob_checker import *"
__all__ = ['check_blob_existence']

# Package version information
__version__ = '0.1.0'