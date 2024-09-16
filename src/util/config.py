import configparser


class ConfigSection:
    def __init__(self,section : configparser.SectionProxy):
        self._dict= {k:v for k,v in section.items() }

    def __iter__(self):
        return iter(self._dict.items())

    def __len__(self):
        return len(self._dict)

    def __contains__(self, key : str):
        return key in self._dict

    def __getattr__(self,key : str):
        try:
            return self._dict[key]
        except Exception as e:
            raise Exception(f'Unknown key {key} in group')

class ConfigValues:
    Fallback = dict(
        daemon = dict(
            ip = '0.0.0.0',
            socket = '8080'
        ),
        battery = dict(
            retain = '7'
        )
    )

    def __init__(self,filename='/etc/defaults/picam.config'):

        self.parser = configparser.ConfigParser()
        self.parser.read_dict(self.Fallback)
        self.parser.read(filename)
        self._sections = { s : ConfigSection(self.parser[s]) for s in self.parser.sections() }

    def __getitem__(self,section : str):
        return self._sections[section]

    def __len__(self):
        return len(self._sections)

    def __contains__(self,section : str):
        return section in self._sections

    def __iter__(self):
        return iter(self._sections)

    def __getattr__(self,section : str):
        try:
            return self[section]
        except Exception as e:
            raise Exception(f'Unknown section {section} in defaults')




