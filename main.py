import requests
from bs4 import BeautifulSoup
from ebooklib import epub
import html2text

def fetch_wechat_article(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"❌ Failed to fetch: {url}")
        return None, None

    soup = BeautifulSoup(resp.text, "html.parser")
    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else "未命名文章"

    # 这里改为用 class="rich_media_content" 查找文章主体
    content_div = soup.find("div", class_="rich_media_content")
    if not content_div:
        print(f"⚠️ 找不到文章内容：{url}")
        return title, None

    html = str(content_div)
    text = html2text.html2text(html)

    return title, text

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

