import configparser
import os

from invoke import task


def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def write_to_bashrc(config, bashrc_path):
    with open(bashrc_path, "a") as bashrc_file:
        for section in config.sections():
            for key, value in config.items(section):
                bashrc_file.write(f"export {key.upper()}={value}\n")


@task
def update_bashrc(ctx, config_path):
    bashrc_path = os.path.expanduser("~/.bashrc")
    config = read_config(config_path)
    write_to_bashrc(config, bashrc_path)
    print(f"Variables from {config_path} have been written to {bashrc_path}")
