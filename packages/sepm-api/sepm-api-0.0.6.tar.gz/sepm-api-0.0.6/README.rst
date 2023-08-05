sepm-api
========

.. image:: https://img.shields.io/pypi/v/sepm-api.svg
    :target: https://pypi.python.org/pypi/sepm-api
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/aalmero/sepm-api.png
   :target: https://travis-ci.org/aalmero/sepm-api
   :alt: Latest Travis CI build status

| This is a wrapper around the Symantec Endpoint Protection Manager REST API.
| This includes some undocumented endpoints, that may not work as expected.
| All the information for the various endpoints were pulled from https://apidocs.securitycloud.symantec.com/.
| If you find any bugs please open an issue or a pull request.

NOTE: The Python wrapper API is work in progress and should be treated as a software in beta, especially regarding the "undocumented" API endpoints.

Usage
-----

    Refer to the `examples <https://github.com/aalmero/sepm-api/tree/main/examples>`_ folder.


Installation
------------

>>>pip install sepm-api

Requirements
^^^^^^^^^^^^

Python :: 3.7+

Environment Variables::

    API_USERNAME
    API_PASSWORD
    API_DOMAIN
    API_BASE_URL  [default: https://localhost:8446/sepm/api/v1]

Compatibility
-------------
Symantec Endpoint Protection Manager API 14.3

License
-------

This software code is license under `MIT <https://github.com/aalmero/sepm-api/blob/main/LICENSE>`_.

Authors
-------

`sepm-api` was written by `Alex Almero <aalmero@gmail.com>`_.

Disclaimers
-----------
I am in no way affiliated with Broadcom. Symantec is a registered trademark by Broadcom.