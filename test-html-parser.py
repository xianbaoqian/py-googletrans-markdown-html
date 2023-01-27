from html.parser import HTMLParser

from utils import Decrepter, Encrepter


class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self._level = 0
        self._output = []
        self._buffer = ""

    def indent(self):
        self._level += 1

    def dedent(self):
        self._level -= 1
        assert self._level >= 0

    def print(self, line, indent=True, newline=True):
        if self._buffer:
            self._output[-1] += self._buffer + line
            self._buffer = ""
        else:
            if newline:
                self._output.append('    ' * self._level + line)
            else:
                self._buffer = line

    def final(self):
        return '\n'.join(self._output)

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag, attrs)
        contents = [tag]
        contents.extend(f'{k}="{v}"' for k, v in attrs)
        if tag not in ['br', 'img']:
            self.print(f'<{" ".join(contents)}>')
            self.indent()
        else:
            self.print(f'<{" ".join(contents)}>', newline=False)

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        self.dedent()
        self.print(f'</{tag}>')

    def handle_data(self, data):
        # Is it safe to always strip?
        trimmed = data.strip()
        if trimmed:
            self.print(trimmed)


parser = MyHTMLParser()
# parser.feed('<html><head id="dudu"><title>Test</title></head>'
#             '<body><h1>Parse me!</h1></body></html>')

with open('test.md') as f:
    content = f.read()

# parser.feed(content)
# print(parser.final())


encrepter = Encrepter()
encrepter.feed(content)
encrepted = encrepter.finalize()


decrepter = Decrepter(encrepter.tags)
decrepter.feed(encrepted)
decrepted = decrepter.finalize()
print(decrepted)
