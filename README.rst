pl-medcon
================================

.. image:: https://badge.fury.io/py/medcon.svg
    :target: https://badge.fury.io/py/medcon

.. image:: https://travis-ci.org/FNNDSC/medcon.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/medcon

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-medcon

.. contents:: Table of Contents


Abstract
--------

An app to covert NIfTI volumes to DICOM files.


Synopsis
--------

.. code::

    python medcon.py                                           \\
        -i | --inputFile					    \\
	[-a]  [--args]						    \\
	[-do]      						    \\
        [-h] [--help]                                               \\
        [--json]                                                    \\
        [--man]                                                     \\
        [--meta]                                                    \\
        [--savejson <DIR>]                                          \\
        [-v <level>] [--verbosity <level>]                          \\
        [--version]    
        <inputDir>
        <outputDir> 

Description
-----------

``medcon.py`` is a ChRIS-based application that takes arguments and converts NIfTI volumes to DICOM images.

Agruments
---------

.. code::

        -i | --inputFile
        Input file to process. This file exists within the explictly provided CLI
        positional <inputDir>.

        [-a]  [--args]	
        Optional string of additional arguments to "pass through" to medcon.

        All the args for medcon are themselves specified at the plugin level with this flag. These
        args MUST be contained within single quotes (to protect them from the shell) and
        the quoted string MUST start with the required keyword 'ARGS: '.

        [-do]  
        Optional argument which an specify a conversion from one type to another. 
        Currently, only supports conversion from NIfTI to DICOM by passing the string "nifti2dicom" 
	
        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit. 

Run
----

This ``plugin`` can be run in two modes: natively as a python package or as a containerized docker image.

Using PyPI
~~~~~~~~~~

To run from PyPI, simply do a 

.. code:: bash

    pip install medcon

and run with

.. code:: bash

    medcon.py --man /tmp /tmp

to get inline help. The app should also understand being called with only two positional arguments

.. code:: bash

    medcon.py /some/input/directory /destination/directory


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

Now, prefix all calls with 

.. code:: bash

    docker run --rm -v $(pwd)/out:/outgoing                             \
            fnndsc/pl-medcon medcon.py                        \

Thus, getting inline help is:

.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-medcon medcon.py                        \
            --man                                                       \
            /incoming /outgoing

Examples
--------





