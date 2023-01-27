Google translate for Markdown / HTML files
==========================================
This library leverages the existing googletrans library to translate Markdown / HTML.

It first encrypt all the HTML tags (so that they're not translated), uses Google Translator to translate the content, then decrypt the content to get back all the HTML tags.

Usage
=====
- In VSCode, open translate.py and change src='en' dest="zh-cn" to your src and dest language pair.
- Install all the dependencies via `pip install -r requirements.txt'
- In the console, run `python translate.py`

To review the diff in VSCode, first click on src.md then click on the dest.md (order matters!) while pressing the Control (on WIn/Linux) / Command (on Mac) key. In the popup menu, click on "Compare selected". The "inline view" can be found after clicking the three dots that you can find from the top right corner.

Tips: you can right click on a line and revert the change if the line doesn't need to be translated (e.g. Citation)