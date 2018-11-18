#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import yaml


class ConfigureLeafSpine():
    """Class to configure and maintain leaf spine switches"""

    def __init__(
            self,
            hosts,
            groups,
            baseconfig,
            spines,
            spineconfig,
            leafs,
            leafconfig
            ):
        with open(hosts) as file1:
            self.hosts = yaml.load(file1)
        with open(groups) as file2:
            self.groups = yaml.load(file2)
        with open(spines) as file3:
            self.spines = yaml.load(file3)
        with open(leafs) as file4:
            self.leafs = yaml.load(file4)
        self.baseconfig = baseconfig
        self.spineconfig = spineconfig
        self.leafconfig = leafconfig
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

    def generatespineconfig(self):
        """Generates the spine configuration"""
        template = self.ENV.get_template(self.spineconfig)
        for key, value in self.hosts.items():
            if value['role'] == 'spine':
                config = template.render(
                    host=value,
                    bgp=self.spines['bgp']
                    )
                filename = 'configs/{0}.config'.format(key)
                with open(filename, 'w') as file:
                    file.writelines(config)

    def generateleafconfig(self):
        """Generates the leaf configuration"""
        template = self.ENV.get_template(self.leafconfig)
        for key, value in self.hosts.items():
            if value['role'] == 'leaf':
                config = template.render(
                    host=value,
                    vlans=self.leafs['vlans'],
                    accessinterfaces=self.leafs['accessinterfaces'],
                    routemaps=self.leafs['routemaps'],
                    bgp=self.leafs['bgp']
                    )
                filename = 'configs/{0}.config'.format(key)
                with open(filename, 'w') as file:
                    file.writelines(config)


if __name__ == "__main__":
    lsconfig = ConfigureLeafSpine(
        'hosts.yaml',
        'groups.yaml',
        'baseconfig.j2',
        'spine.yaml',
        'spine.j2',
        'leaf.yaml',
        'leaf.j2'
    )
    lsconfig.generatebaseconfig()
    lsconfig.generatespineconfig()
    lsconfig.generateleafconfig()
