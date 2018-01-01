"""Functions for creating, managing, and dealing with configs for window placements."""

import configparser
from subprocess import call
import sys

# try:
#     from api import move, explicit_move
# except ModuleNotFoundError:
#     from pystiler.api import move, explicit_move

CONFIG_FILE = '/home/riley/.pystiler.ini'

def parse_config(section):
    """prec: config section name
    postc: string shell command that will create and move windows."""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if not config.has_section(section):
        print(f"Workspace '{section}' could not be found!")
        sys.exit(1)

    mode = config.get(section, 'mode')
    if mode == 'simple':
        specific = translate_simple_specific(config, section)
    elif mode == 'specific':
        specific = config[section]
    elif mode == 'explicit':
        commands = []
        applist = eval(config[section]['applist'])
        for app in applist:
            commands.append(app['application'])
            locs = ['screen_columns', 'screen_rows', 'first_column', 'last_column', 'first_row', 'last_row']
            commands.append('pyst explicit ' + ' '.join([str(app['applocation'][loc]) for loc in locs]))
        return '; '.join(commands)
    else:
        print(f"Mode '{mode}' not supported yet.")
        sys.exit(1)
    # Build up shell commands
    # Requires pyst (this module) to be installed
    # hot tip don't put python code in your config file it'll get parsed
    commands = []
    for command_parts in specific['applist']:
        commands.append(command_parts['application'])
        commands.append('pyst move ' + command_parts['applocation'])

    return '; '.join(commands)


def translate_simple_specific(config, section):
    """Turn a simple config into a specific one."""
    simple_dict = config._sections[section]
    specific_dict = {'mode': 'specific', 'applist': []}

    for location in eval(simple_dict['applocation']):
        app_item = {
            'application': simple_dict['application'],
            'terminalDir': simple_dict['terminaldir'],
            'applocation': location}
        specific_dict['applist'].append(app_item)


    return specific_dict



def make_example_config():
    """Define a working example config, and write it to ~/.pystiler.ini"""
    config = configparser.ConfigParser()
    # Only one application, only named locations
    config['example_simple'] = {
        'mode': 'simple',
        'application': 'xfce4-terminal',
        'terminaldir': '~/Projects',
        'applocation': ['top_left', 'bottom_left', 'right']}

    # >1 applications, only named locations
    config['example_specific'] = {'mode': 'specific',
                                  'appList': [{'application': 'xfce4-terminal',
                                               'terminaldir': '~/Projects',
                                               'applocation': 'top_left'},
                                              {'application': 'xfce4-terminal',
                                               'terminaldir': '~/Downloads',
                                               'appLocation': 'right'}]}
    # >1 applications, any locations
    config['example_explicit'] = {'mode': 'explicit',
                                  'applist': [{'application': 'xfce4-terminal',
                                               'terminaldir': '/etc',
                                               'applocation': {'screen_columns': 3,
                                                               'screen_rows'   : 3,
                                                               'first_column'  : 1,
                                                               'last_column'   : 1,
                                                               'first_row'     : 1,
                                                               'last_row'      : 3}},
                                              {'application': 'xfce4-terminal',
                                               'terminaldir': '~/',
                                               'applocation': {'screen_columns': 3,
                                                               'screen_rows'   : 3,
                                                               'first_column'  : 2,
                                                               'last_column'   : 2,
                                                               'first_row'     : 1,
                                                               'last_row'      : 3}}]}
    return write_config(config)


def write_config(config):
    """Logic to write a config file to disk, without erasing unmodified sections."""
    parser = configparser.ConfigParser()
    parser.read(CONFIG_FILE)

    for section in config.sections():
        if not parser.has_section(section):
            parser.add_section(section)
        for option in config.options(section):
            value = config.get(section, option)
            parser.set(section, option, value)

    with open(CONFIG_FILE, 'w') as configfile:
        parser.write(configfile)


def run_config(section):
    """Run a predefined workspace (section) from the config file."""
    call(parse_config(section), shell=True)


if __name__ == '__main__':
    run_config('example_simple')
