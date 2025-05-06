Usage
=====

Basic Concepts
--------------

Config Engine works defining configuration options in a consistent manner by
registering :py:class:`~conf_engine.options.Option` objects to a
:py:class:`~conf_engine.configuration.Configuration` object.  The Option
objects can represent a particular option type and may have their own options
for defining constraints on the option values.  For example a
:py:class:`~conf_engine.options.NumberOption` has the ability to define a range
using minimum and maximum values.

A :py:class:`~conf_engine.configuration.Configuration` does not need to have
all options registered before attempting to read configuration.  This allows
individual modules and libraries that share the use of Config Engine to be
able to register their own option sets independently as long as they do not
have name conflicts.

Registering and Reading Options
-------------------------------

While it is possible to have multiple instances of the
py:class:`~conf_engine.configuration.Configuration` object, it's typically
not needed.  Most use cases can take advantage of the module level object.
In the below example the module level object is used to register a string
option for both a username and password.

.. literalinclude:: examples/register.py
   :language: python
   :caption: Registering and reading options.

In the above example a debug mode option is also registered with a default
value of `False`.  Default values will be returned if a value for the option
cannot be found in any of the configuration sources.

Option Groups
-------------

Groups can be used to organize options with a similar purpose.  For example
an application may need to access two different APIs.  By utilizing groups
the credentials for each API can be defined separately using similar naming
semantics.

.. literalinclude:: examples/groups.py
   :language: python
   :caption: Registering and accessing option groups.

Creating and Consuming Configuration
------------------------------------

Configuration data can be consumed by Config Engine from either operating
system environment variables or from `ini` style files.  When consuming from
environment variables options names are capitalized and prepended with their
group name followed by an ``_`` character.  For `ini` style configuration
all options must be defined in sections.  The section name corresponds with
the option group and the ``[DEFAULT]`` section is used for any options
defined with no group.

By default Config Engine will look int the current working directory for
any files with the ``.ini`` extension and load them as configuration.
However it is possible to define the location of configuration data by using
the ``--config-file`` and ``--config-directory`` CLI options when starting
your application.

Configuration Data Caching
--------------------------

By default Config Engine will store the value of a configuration option
once it has been read from the configuration source.  However, this
caching behavior can be disabled by passing `cache=False` when creating
a :py:class:`~conf_engine.configuration.Configuration` object, or a
:py:class:`~conf_engine.configuration.ConfigGroup`.

Cached data can also be invalidated by calling the `flush_cache()`
method on either the :py:class:`~conf_engine.configuration.Configuration`
object, or the :py:class:`~conf_engine.configuration.ConfigGroup` as
well.

.. literalinclude:: examples/caching.py
   :language: python
   :caption: Registering and accessing option groups.

Namespaces
----------

The environment parser supports an optional namespace which will
prepend each option with the namespace and an underscore to help
ensure that the given option doesn't have a name collision with other
unrelated environment variables.  Namespaces require the use of a
declared configuration object rather than using the one provided
in the ConfEngine module.  Declaring options and accessing option
values through the configuration object remains unchanged.

.. literalinclude:: examples/namespaces.py
   :language: python
   :caption: Using namespaces.