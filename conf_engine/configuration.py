import logging

import conf_engine.core.exceptions as cfg_exc
import conf_engine.parsers as parsers

from typing import Union

from conf_engine.options import Option, UNDEFINED

REGISTERED_PARSERS = [
    parsers.CLIParser,
    parsers.EnvironmentParser,
    parsers.INIFileParser,
]


class ConfigGroup:
    def __init__(self, name: Union[str, None],
                 namespace: str = None, cache: bool = True):
        """
        A collection of related configuration options.

        :param name: The configuration group name.
        :param namespace: Namespace is passed through to parsers that support
            it.  See :py:meth:`__init__()` docs for the parser class
            for more details.
        :param cache: When True (default) this ConfigGroup will store
            values after they are read from configuration.
        """
        self._name = name
        self._namespace = namespace
        self._cache = cache
        self._opt_cache = {}
        self._value_cache = {}

    def __getattr__(self, item: str):
        return self._get_option(item)

    def __contains__(self, item):
        return item in self._opt_cache

    def _get_option(self, option: str):
        if option in self._opt_cache:
            return self._get_option_value(self._opt_cache[option], self._name)
        raise cfg_exc.UnregisteredOption(option)

    def _cache_option_value(self, name, value):
        self._value_cache[name] = value

    def _get_option_value_from_cache(self, name):
        return self._value_cache[name]

    def _option_value_cached(self, name):
        return name in self._value_cache if self._cache else False

    def _get_option_value(self, option: Option, group):
        if self._option_value_cached(option.name):
            return self._get_option_value_from_cache(option.name)
        else:
            return self._get_option_value_from_source(option, group)

    def _get_option_value_from_source(self, option: Option, group):
        for parser in REGISTERED_PARSERS:
            try:
                parser = parser(namespace=self._namespace)
                value = parser.get_option_value(option, group)
                # Validate the value is correctly formatted.
                value = option.option_type(value)
                # Store the value in the value cache.
                self._cache_option_value(option.name, value)
                # The first parser in registered parsers list
                # should take precedence, so we return early.
                return value
            except cfg_exc.ValueNotFound:
                continue
            except Exception as e:
                logging.exception(e)
                raise e

        if option.default is not UNDEFINED:
            return option.option_type(option.default)
        # If we get here, then we've not found the value.
        fq_name = option.name
        if self._name:
            fq_name = self._name + '.' + fq_name
        raise cfg_exc.ValueNotFound(fq_name)

    def flush_cache(self, name: str = None):
        """
        Flush the value cache and read from configuration source on
        next access.
        :param name: If name is provided, only the value for the named
        option is flushed.
        :return:
        """
        if name:
            self._value_cache.pop(name)
        else:
            self._value_cache = {}

    def register_options(self, options: [Option]):
        for option in options:
            self.register_option(option)

    def register_option(self, option: Option):
        if option.name in self._opt_cache and option != self._opt_cache[option.name]:
            raise cfg_exc.DuplicateOptionError(option.name)
        self._opt_cache[option.name] = option


class Configuration:
    def __init__(self, namespace: str = None, cache: bool = True):
        """
        Configuration object that represents the configuration of the
        application.

        :param namespace: Namespace is passed through to parsers that support
            it.  See :py:meth:`__init__()` docs for the parser class
            for more details.
        :param cache: When True (default) Config Engine will read the
            value of the option from the configuration source once, and
            then store the value for subsequent lookups.  If False,
            then the value is not stored and is always read from the
            configuration source.  When set here, ConfigEngine will set
            pass this along to auto created configuration groups.
        """
        self._cache = cache
        self._group_cache = {None: ConfigGroup(None, namespace=namespace)}
        self._namespace = namespace

    def __getattr__(self, item):
        return self._get_group(item)

    def __contains__(self, item):
        return item in self._group_cache

    def register_options(self, options: [Option], group: str = None):
        """
        Register bulk options with the config.
        :param options: List of options.
        :param group: Group name to which options are added.
        :return:
        """

        for option in options:
            self.register_option(option, group=group)

    def flush_cache(self):
        """
        Signal all configuration groups to flush their cache and
        read from configuration source on next access.
        """
        for _, group in self._group_cache.items():
            group.flush_cache()

    def register_option(self, option: Option, group: str = None, create_group: bool = True):
        """
        Register options with the config.  If group is specified, the options are
        added to the option group, otherwise options are registered to the base object.
        :param option: Option to register.
        :param group: Group name to which the option is added.
        :param create_group: Create the group if not already registered.
        :return:
        """
        if group and group not in self._group_cache:
            if create_group:
                self._group_cache[group] = ConfigGroup(group,
                                                       namespace=self._namespace,
                                                       cache=self._cache)
            else:
                raise cfg_exc.UnregisteredGroup(group)
        self._group_cache[group].register_option(option)

    @property
    def registered_parsers(self):
        return self._registered_parsers

    def _get_group(self, group: str):
        """
        Get group by its name as called during attribute access against the
        configuration object.  If the option cannot be found an UnregisteredOption
        error will be raised.

        If the option matches a group name, the group object is returned and the
        subsequent attribute access is handled by the group object.
        """
        # If we find the option name in our cache, that means what was passed to
        # __getattr__() is the group value.  We return that and have the group object
        # perform the call to _get_option_value().  Otherwise, we return the default
        # group object

        if group in self._group_cache:
            return self._group_cache[group]
        else:
            return getattr(self._group_cache[None], group)
