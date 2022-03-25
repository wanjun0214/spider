import re
import requests
import execjs


session = requests.session()
session.headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}
base_url = 'https://www.zhihu.com/search?q=python&type=content'
resp = session.get(url=base_url)
# print(resp.cookies['d_c0'])
js_initialData = re.findall('<script id="js-initialData" type="text/json">(.*?)</script>', resp.text)[0]
# print(js_initialData)
# print(resp.text)


content_url = 'https://www.zhihu.com/api/v4/search_v3?t=general&q=python&correction=1&offset=20&limit=20&filter_fields=&lc_idx=20&show_all_topics=0&search_source=Normal'
with open('zhihu.js', mode='rt', encoding='utf-8') as f1:
    signature = execjs.compile(f1.read()).call('x_zse_96', resp.cookies['d_c0'])
with open('zhihu.js', mode='rt', encoding='utf-8') as f2:
    params = execjs.compile(f2.read()).call('generate_params', js_initialData)
# print(signature)
# print(params)
session.headers.update({
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "referer": "https://www.zhihu.com/search?q=python&type=content",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
    "x-ab-param": params['X-Ab-Param'],
    "x-ab-pb": params['X-AB-PB'],
    "x-api-version": "3.0.91",
    "x-app-za": "OS=Web",
    "x-requested-with": "fetch",
    "x-zse-93": "101_3_2.0",
    "x-zse-96": signature
})
content_data = session.get(url=content_url)
print(content_data.json())
