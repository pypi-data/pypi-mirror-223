import feedparser
import pprint
import json

# 网站种子解析
# rss_oschina = feedparser.parse("https://rustcc.cn/rss")
# rss_oschina = feedparser.parse("https://lijc210.gitee.io/rss.xml")
rss_oschina = feedparser.parse("https://rsshub.app/infzm/2")
# 抓取内容 ， depth 抓取深度
pprint.pprint(rss_oschina, depth=2)
print(rss_oschina["feed"]["title"])

for entry in rss_oschina["entries"]:
    print(json.dumps(entry))
    print(entry["title"])
    print(entry["summary"])
    print(entry["published"])
