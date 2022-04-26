from configparser import ConfigParser

config = ConfigParser()
config['DB'] = {
    'HOST': 'localhost',
    'DATABASE': 'datatrackdb',
    'USER': 'root',
    'PASSWORD': 'password',
    'PORT': '3306',
}
with open('application\\config\\config.ini', 'w') as output_file:
    config.write(output_file)