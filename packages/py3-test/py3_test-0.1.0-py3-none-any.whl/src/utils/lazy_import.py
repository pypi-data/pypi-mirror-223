"""
@File    :   lazy_import.py
@Time    :   2021/03/12 14:43:29
@Author  :   lijc210@163.com
@Desc    :   None
"""


class LazyImport:
    def __init__(self, module_name):
        self.module_name = module_name
        self.module = None

    def __getattr__(self, name):
        if self.module is None:
            self.module = __import__(self.module_name)
        return getattr(self.module, name)
