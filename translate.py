from googletrans import Translator
translator = Translator()


with open('0_src.md') as f:
    content = f.read()


from utils import Decrepter, Encrepter


encrepter = Encrepter()
encrepter.feed(content)
encrepted = encrepter.finalize()


# Translation
lines = encrepted.split("\n")

def split(list_a, chunk_size):

  for i in range(0, len(list_a), chunk_size):
    yield list_a[i:i + chunk_size]

outputs = []
for chunk in split(lines, 100):
   txt = '\n'.join(chunk)
   out = translator.translate(txt, src='en', dest="zh-cn")
   outputs.append(out.text)
translated = '\n'.join(outputs)

# print(translated)

# back
decrepter = Decrepter(encrepter.tags)
decrepter.feed(translated)
decrepted = decrepter.finalize()
print(decrepted)


with open('1_dest.md', 'w') as f:
    f.write(decrepted)

