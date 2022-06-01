from conf_engine import config
from conf_engine import options

# Create option list.
api1_options = [
    options.StringOption('api_url'),
    options.StringOption('token')
]
api2_options = [
    options.StringOption('api_url'),
    options.StringOption('token'),
    options.NumberOption('version')
]

# Register options.
config.register_options(api1_options, group='api1')
config.register_options(api2_options, group='api2')

# Read option values.
api1_username = config.api1.username
api2_version = config.api2.version

