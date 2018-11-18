#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import yaml


class ConfigureLeafSpine():
    """Class to configure and maintain leaf spine switches"""

    def __init__(
            self,
            hosts,
            groups,
            baseconfig
            ):
        with open(hosts) as file1:
            self.hosts = yaml.load(file1)
        with open(groups) as file2:
            self.groups = yaml.load(file2)
        self.baseconfig = baseconfig
        self.ENV = Environment(loader=FileSystemLoader('.'))

    def generatebaseconfig(self):
        """Generates base configuration files"""
        template = self.ENV.get_template(self.baseconfig)
        for key, value in self.hosts.items():
            config = template.render(
                defaults=self.groups['defaults'],
                hostname=key,
                host=value,
                site=self.groups[value['site']]
            )
            filename = 'configs/{0}-base.config'.format(key)
            with open(filename, 'w') as file:
                file.writelines(config)


if __name__ == "__main__":
    lsconfig = ConfigureLeafSpine(
        'hosts.yaml',
        'groups.yaml',
        'baseconfig.j2'
    )
    lsconfig.generatebaseconfig()
