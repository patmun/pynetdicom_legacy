.. _getting_started:

===============
Getting Started
===============

Introduction
============
pynetdicom is a pure python_ package implementing the DICOM network
protocol. It uses the pydicom package.

pynetdicom makes it easy to create DICOM clients (SCUs) or servers
(SCPs). The following service classes are currently supported, both as
SCU and SCP:

  * Verification
  * Storage
  * Query/Retrieve

pynetdicom is easy to install and use, and because it is a pure 
python package, it should run anywhere python runs. 

You can find examples in :ref:`here <usecases>`.

pynetdicom is hosted `here <https://github.com/patmun/pynetdicom>`_.

License
=======
pynetdicom uses the `MIT license 
<https://github.com/patmun/pynetdicom/blob/master/LICENCE.txt>`_.

Prerequisites
=============
* python_ 2.4 and higher
* pydicom_ 0.9.7 and above


Installation
============
Here are the installation options:

  * pynetdicom is registered at PyPi_, so it can be installed with pip_::

        pip install pynetdicom

  * download the `source package <https://pypi.python.org/pypi/pynetdicom>`_ ,
    uncompress and install with::

        python setup.py install    

  * A `windows installer <https://pypi.python.org/packages/84/48/412cec48bfe71a6dc753806c1417690900efe06339ae6136e2769abd2277/pynetdicom-0.8.1.win32.exe#md5=1bb36733371614a9811506f935268ae1>`_ is also available.

  * To get the latest revision you can clone the `source tree <http://code.google.com/p/pynetdicom/source>`_
    with::

        hg clone https://github.com/patmun/pynetdicom 


Support
=======

Please join the `pynetdicom discussion group
<https://groups.google.com/forum/#!forum/pynetdicom>`_ to ask questions, give
feedback, post example code for others -- in other words for any
discussion about the pynetdicom code. New versions, major bug fixes,
etc.  will also be announced through the group.



.. _python: https://www.python.org
.. _pydicom: https://github.com/darcymason/pydicom
.. _pip: https://pypi.python.org/pypi/pip
.. _PyPi: https://pypi.python.org/pypi
