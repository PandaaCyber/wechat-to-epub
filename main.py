import requests
from ebooklib import epub
import html2text

def fetch_wechat_article(url):
    api_url = "https://api.tianapi.com/wxnew/?key=YOUR_API_KEY&url=" + url
    # 这里用天行数据微信公众号文章接口，免费额度有限，可以申请免费key

    try:
        resp = requests.get(api_url, timeout=10)
        data = resp.json()
        if data.get("code") != 200:
            print(f"❌ API返回错误：{data.get('msg')}")
            return None, None

        newslist = data.get("newslist")
        if not newslist or len(newslist) == 0:
            print("❌ API未返回文章内容")
            return None, None

        article = newslist[0]
        title = article.get("title", "未命名文章")
        content = article.get("content", "")
        text = html2text.html2text(content)
        return title, text

    except Exception as e:
        print(f"❌ 请求API失败：{e}")
        return None, None

def create_epub(title, content, filename="output.epub"):
    book = epub.EpubBook()
    book.set_identifier("wechat-article")
    book.set_title(title)
    book.set_language("zh")

    c1 = epub.EpubHtml(title=title, file_name="chap_1.xhtml", lang="zh")
    c1.content = f"<h1>{title}</h1><pre>{content}</pre>"

    book.add_item(c1)
    book.toc = (epub.Link("chap_1.xhtml", title, "chap_1"),)
    book.add_item(epub.EpubNavi())
    book.add_item(epub.EpubNCX())

    book.spine = ["nav", c1]
    epub.write_epub(filename, book)

def main():
    with open("input.txt", "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    if not urls:
        print("❌ input.txt 为空，未提供任何链接")
        return

    for url in urls:
        print(f"🚀 正在处理：{url}")
        title, content = fetch_wechat_article(url)
        if content:
            create_epub(title, content)
            print(f"✅ 已生成 EPUB：{title}")
        else:
            print(f"❌ 内容为空，跳过：{url}")

if __name__ == "__main__":
    main()


