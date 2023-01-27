from html.parser import HTMLParser


class Encrepter(HTMLParser):

    def __init__(self):
        super(Encrepter, self).__init__()
        self.tags = []
        self.content = []

    def print(self, line):
        self.content.append(line)

    def finalize(self):
        return ''.join(self.content)

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag, attrs)
        # Handle img alt here
        self.tags.append((tag, attrs))
        self.print('<NOP>')

    def handle_endtag(self, tag):
        self.tags.append(tag)
        self.print('</NOP>')

    def handle_data(self, data):
        self.print(data)


class Decrepter(HTMLParser):

    def __init__(self, tags):
        super(Decrepter, self).__init__()
        self.tags = tags
        self.cur_tag = 0
        self.content = []

    def print(self, line):
        self.content.append(line)

    def finalize(self):
        return ''.join(self.content)

    def next_tag(self):
        output = self.tags[self.cur_tag]
        self.cur_tag += 1
        return output

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag, attrs)
        tag, attrs = self.next_tag()
        contents = [tag]
        contents.extend(f'{k}="{v}"' for k, v in attrs)
        self.print('<' + ' '.join(contents) + '>')

    def handle_endtag(self, tag):
        tag = self.next_tag()
        self.print(f'</{tag}>')

    def handle_data(self, data):
        self.print(data)
