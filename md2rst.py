# -*- coding: utf-8 -*-

try:
    import pypandoc
except ImportError:
    print("pypandoc not available!!")
    exit("First install pypandoc. Ex: \"pip install pypandoc\"")


long_description = pypandoc.convert('README.md', 'rst', outputfile='README.md2rst')
