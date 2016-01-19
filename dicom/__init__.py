from __future__ import absolute_import

try:
    from pydicom import *
    from pydicom import __version_info__
except ImportError:
    from dicom import *
    from dicom import __version_info__
