from config_engine import Configuration
from config_engine import options

# Create option list.
cache_options = [
    options.StringOption('username'),
    options.StringOption('password'),
]

no_cache_options = [
    options.BooleanOption('debug', default=False)
]

# Create two configuration groups, one that caches, and one that does not.
# Then register the options.
caching_config = Configuration(cache=True)
no_cache_config = Configuration(cache=False)
caching_config.register_options(cache_options)
no_cache_config.register_options(no_cache_options)

# This will only read from source once, and then use that
# value in subsequent lookups
print(caching_config.username)

# This will only read from configuration source, and never
# from the cache.
print(no_cache_options.debug)


