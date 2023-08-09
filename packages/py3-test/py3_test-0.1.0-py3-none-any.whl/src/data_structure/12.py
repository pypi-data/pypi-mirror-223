"""
@author: lijc210@163.com
@file: 12.py
@time: 2020/06/22
@desc: 功能描述。
"""
BRANKETS = {"}": "{", "]": "[", ")": "("}
BRANKETS_LEFT, BRANKETS_RIGHT = BRANKETS.values(), BRANKETS.keys()


def bracket_check(string):
    stack = []
    for char in string:
        if char in BRANKETS_LEFT:
            stack.append(char)
        elif char in BRANKETS_RIGHT:
            if stack and stack[-1] == BRANKETS[char]:
                stack.pop()
            else:
                return False
        else:
            return False
    return not stack


print(bracket_check("(())[]{}"))
