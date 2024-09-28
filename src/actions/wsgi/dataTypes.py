from sympy.codegen.cnodes import static


class CSV:
    def __init__(self,fields=[],separator=',',quote="'"):
        self.fields=fields
        self.separator = separator
        self.quote=quote

    def _quote(self,x):
        s=str(x)
        return f'{self.quote}{s}{self.quote}' if ' ' in s else s

    def _row(self,items):
        strs = [self._quote(i) for i in items]
        return self.separator.join(strs)

    def __call__(self,rows):
        lines = [self._row(r) for r in rows]
        lines.insert(0,self._row(self.fields))
        return '\n'.join(lines)

