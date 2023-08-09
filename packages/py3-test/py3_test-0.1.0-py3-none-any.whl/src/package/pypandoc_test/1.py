import pypandoc

# coding: utf-8
"""
@File    :   1.py
@Time    :   2023/05/09 11:24:22
@Author  :   lijc210@163.com
@Desc    :   None
pip install pypandoc_binary
convert_text
convert_file
"""
import pypandoc

# # md to html
# output = pypandoc.convert_file(m_input, "html", format="md", outputfile="results.html")

# md to html
output = pypandoc.convert_file(
    "src/package/pypandoc_test/1.html",
    "md",
    format="html",
    outputfile="results.md",
    extra_args=["--extract-media=src"],
)
print(output)

# output = pypandoc.convert_text("# some title", "rst", format="md")
# print(output)
