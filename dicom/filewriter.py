try:
    from pydicom.filewriter import *
except ImportError:
    from dicom.filewriter import *
