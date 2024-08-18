import json
from enum import Enum
from types import NoneType

def asString(value):
    t = type(value)
    if t == int or t == float:
        return str(value)
    elif t == str:
        return f'"{value}"'
    elif t == bool:
        return 'true' if value else 'false'
    elif t == NoneType:
        return 'null'
    elif t == list:
        items = [asString(v) for v in value]
        joined = ','.join(items)
        return f'[{joined}]'
    elif t == dict:
        return formatAsJavaScript(value)
    else:
        return f'"{str(value)}"'


def formatAsJavaScript(obj = {}):
    lines = []
    for key,value in obj.items():
        v = asString(value)
        lines.append(f'{key}: {v}')
    joined = ','.join(lines)
    return '{'+joined+'}'

for d in [{ 'fred' : 7, 'is' : 'noun', 'dead': True },{ 'fred' : [1,2,3], 'is' : None, 'dead': { 'really' : False}}]:
    x = formatAsJavaScript(d)
    print(x)





class OutputFormat(Enum):
    Dictionary = 0
    JavaScript = 1
    JSON = 2

    def format(self,obj = {}):
        if self == OutputFormat.Dictionary:
            return obj
        elif self == OutputFormat.JSON:
            return json.dumps(obj)
        elif self == OutputFormat.JavaScript:
            return formatAsJavaScript(obj)

