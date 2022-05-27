Installation
============

The conf_engine module may be directly from Github via Pip or manually.

Pip Install
-----------

There are two ways to install the module via Pip:  Via PyPI, or install
directly from `Github <https://github.com`.

.. code-block:: shell
   :caption: Install from PyPI

    ~/# pip install conf-engine

.. code-block:: shell
   :caption: Install direct from Github.

    ~/# pip install git+https://github.com/Connectira/conf-engine

Manual Install
--------------

Manual installation is also possible if a machine does not have access directly to Github, or does not have Pip
installed.

.. code-block:: shell
   :caption: Manual install from tarball.

    ~/# unzip conf-engine*.zip
    ~/# cd conf_engine
    ~/conf_engine/# python ./setup.py

If you are looking to install for development you can use `develop` mode with Python's `setuptools` package.

.. code-block:: shell
   :caption: Development install.

    ~/conf_engine/# python ./setup.py develop




