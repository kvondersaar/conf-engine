from config_engine import config
from config_engine import options

# Create option list.
options = [
    options.StringOption('username'),
    options.StringOption('password')
]

# Register options.
config.register_options(options)

# Read option values.
username = config.username
password = config.password


