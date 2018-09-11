import ssl
import time
import os
import urllib.request
import asyncio
import re
from bs4 import BeautifulSoup

def title_getter():
    #SSLエラー回避
    ssl._create_default_https_context = ssl._create_unverified_context
    #入力に成功するまでやり直すため、whileで無限ループ
    while True:
        try:
            print("urlを入力")
            url = input()
            html = urllib.request.urlopen(url).read().decode('utf-8','ignore')
            soup = BeautifulSoup(html,"lxml")
        except:
            print("正しいURLを入力してください。")
        else:
            break
    return soup

def make_dir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        print("ディレクトリ名が重複しています。\nすでに存在するディレクトリの名前を変更します。ユニークな名前を入力してください。")
        new_name = input()
        os.rename(path,"./{}".format(new_name))
        os.mkdir(path)

async def scraping_page():
    soup = title_getter()

    pattern = re.compile(r'productId: "(.*?)"',re.MULTILINE | re.DOTALL)
    pid_get = soup.find('script',text=pattern)

    productId = pattern.search(pid_get.text).group(1)
    print(productId)
    dir_path = "./{}".format(productId)
    make_dir(dir_path)

    sticker_id = re.compile(r'ids:(.*?)]',re.MULTILINE | re.DOTALL)
    ids = sticker_id.search(pid_get.text).group(1).replace("[","").replace(" ","")
    id_list = ids.split(",")
    for download_id in id_list:
        dst_path = os.path.join(dir_path,download_id) + ".png"
        download_url = "https://stickershop.line-scdn.net/stickershop/v1/sticker/{}/ANDROID/sticker.png;compress=true".format(download_id)
        await image_get(download_url,dst_path)

async def image_get(download_url,dst_path):
    try:
        data = urllib.request.urlopen(download_url).read()
        with open(dst_path,mode="wb") as f:
            f.write(data)
    except urllib.error.URLError as e:
            print(e)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scraping_page())
    loop.close()

if __name__ == '__main__':
    main()
