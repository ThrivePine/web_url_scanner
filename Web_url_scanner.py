import random
import requests
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor

def user_agent():
    user_agent_list=["Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.84",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.83",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36",
]
    ua=random.choice(user_agent_list)
    return ua
# def proxy(proxy_name):
#

def read_url(file_name):
    urls=[]
    with open(file_name,'r') as f:
        for url_line in f:
                url=url_line.strip()
                if url.startswith('http://') or url.startswith('https://'):
                    urls.append(url)
                else:
                    # 检查网站是否支持https协议
                    try_https_url = 'https://' + url
                    #这里尝试用https请求如果成功则添加到urls，失败则用http
                    try:
                        requests.head(try_https_url)
                        urls.append(try_https_url)
                    except requests.exceptions.RequestException:
                        urls.append('http://' + url)

        return urls
def scan_url(url, headers):
    try:
        response = requests.get(url=url, headers=headers,timeout=3)
        if response.status_code != 200:
            print(f"\033[1;37;43m[!]\033[0m{url} 状态码: {response.status_code}",flush=True)
        else:
            print(f"\033[1;37;42m[+]\033[0m{url} 状态码: {response.status_code}",flush=True)
    except requests.exceptions.RequestException as e:
        print(f"\033[1;37;41m[-]\033[0m{url} 请求出错",flush=True)
    except requests.exceptions.Timeout:
        print(f"\033[1;37;41m[-]\033[0m{url} 请求超时",flush=True)
    sys.stdout.flush()
def Request():
        file_name= argparse.ArgumentParser()
        file_name.add_argument("-r",help="url file")
        args=file_name.parse_args()
        urls=read_url(args.r)
        ua=user_agent()
        headers={'user-agent':ua}
        with ThreadPoolExecutor(max_workers=100) as e:
            f = [e.submit(scan_url, url, headers) for url in urls]
            for th in f:
                th.result()
if __name__ == '__main__':
    Request()
