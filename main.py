from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ebooklib import epub
import html2text

def fetch_wechat_article(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 15)
        # 等待标题出现
        title_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.rich_media_title')))
        title = title_element.text.strip()

        # 等待内容区出现
        content_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.rich_media_content')))
        content_html = content_element.get_attribute('innerHTML')

    except Exception as e:
        print(f"❌ 抓取元素失败: {e}")
        driver.quit()
        return None, None

    driver.quit()
    text = html2text.html2text(content_html)
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



