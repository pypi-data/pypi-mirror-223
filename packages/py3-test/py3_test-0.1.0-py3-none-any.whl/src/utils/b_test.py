import json

d = {
    b"info:category_name1": b"\xe7\xab\xa3\xe5\xb7\xa5\xe9\xaa\x8c\xe6\x94\xb6",
    b"info:category_name2": b"\xe8\xa3\x85\xe4\xbf\xae\xe5\x90\x88\xe5\x90\x8c",
    b"info:category_name3": b"\xe5\xb7\xa5\xe9\x95\xbf",
    b"info:category_name4": b"",
    b"info:category_name5": b"",
    b"info:category_one1": b"\xe8\xa3\x85\xe4\xbf\xae\xe9\x98\xb6\xe6\xae\xb5",
    b"info:category_one2": b"\xe6\x9c\x8d\xe5\x8a\xa1\xe4\xbf\x9d\xe9\x9a\x9c",
    b"info:category_one3": b"\xe6\x9c\x8d\xe5\x8a\xa1\xe4\xbf\x9d\xe9\x9a\x9c",
    b"info:category_one4": b"",
    b"info:category_one5": b"",
    b"info:category_two1": b"\xe7\xab\xa3\xe5\xb7\xa5\xe9\xaa\x8c\xe6\x94\xb6",
    b"info:category_two2": b"\xe8\xa3\x85\xe4\xbf\xae\xe5\x90\x88\xe5\x90\x8c",
    b"info:category_two3": b"\xe5\xb7\xa5\xe9\x95\xbf",
    b"info:category_two4": b"",
    b"info:category_two5": b"",
    b"info:page_id": b"256194",
    b"info:page_type": b"quality_v9_news",
}

print(json.dumps({k.decode(): v.decode() for k, v in d.items()}, ensure_ascii=False))
