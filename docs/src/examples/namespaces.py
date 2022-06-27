"""
Export your var before running the script.

.. code-block:
    ~# export TESTNS_MYGROUP_MY_VAR=namespaces
"""

from conf_engine import Configuration, options

# Create config object.
config = Configuration(namespace='testns')
# Register options.
config.register_option(options.StringOption('my_var'))

assert config.my_var == 'namespaces'


