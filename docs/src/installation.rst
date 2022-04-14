Installation
============

The config_engine module may be directly from Github via Pip or manually.

Pip Install
-----------

There are two ways to install the module via Pip:  Clone the repository and install from the local copy, or install
directly from `Github <https://github.com`.

.. code-block:: shell
   :caption: Install from clone.

    ~/# git clone https://github.com/Connectria/config-engine
    ~/# cd config_engine
    ~/config_engine/# pip install .

.. code-block:: shell
   :caption: Install direct from Github.

    ~/# pip install git+https://github.com/Connectira/config-engine

Manual Install
--------------

Manual installation is also possible if a machine does not have access directly to Github, or does not have Pip
installed.

.. code-block:: shell
   :caption: Manual install from tarball.

    ~/# unzip config-engine.zip
    ~/# cd config_engine
    ~/config_engine/# python ./setup.py

If you are looking to install for development you can use `develop` mode with Python's `setuptools` package.

.. code-block:: shell
   :caption: Development install.

    ~/config_engine/# python ./setup.py develop




