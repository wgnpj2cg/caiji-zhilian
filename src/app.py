import os

import requests
from flask import Flask
from lxml import etree

PORT = os.getenv("PORT")
app = Flask(__name__)
url = "https://so.iqiyi.com/so/q_"


def search(name):
    ret_list = []
    url_s = url + name
    response = requests.get(url_s).text
    k = etree.HTML(response)
    result_list = k.xpath('//div[@desc="card"]')
    for x in result_list:
        ret = {}
        try:
            leixing = x.xpath('.//div/div[2]/h3/span/text()')[0]
            if leixing:
                print(leixing)
                ret["type"] = leixing

                ret["title"] = "".join(x.xpath('.//div/div[2]/h3/a//span/text()'))
                ret["source"] = "".join(x.xpath('.//em[@class="player-name"]//text()'))
                album_list = x.xpath('.//ul[@class="album-list"]//li')
                result_list = []
                pre_num = 0
                for album in album_list:
                    j = "".join(album.xpath('.//a/@title'))
                    print(j)
                    if leixing == "综艺":
                        if str(album.xpath('.//@href')[0]).startswith("//"):
                            u = 'https://' + str(album.xpath('.//@href')[0])[2:]
                        else:
                            u = str(album.xpath('.//@href')[0])
                        result_list.append({
                            j: u
                        })
                        continue

                    i = "".join(album.xpath('.//a/span/text()')).replace(" ", "").replace("\n", "")
                    if i == "...":
                        result_list = []
                        pre_num = 0
                        continue
                    if int(i) == pre_num + 1:
                        if str(album.xpath('.//@href')[0]).startswith("//"):
                            u = 'https://' + str(album.xpath('.//@href')[0])[2:]
                        else:
                            u = str(album.xpath('.//@href')[0])
                        result_list.append({
                            j: u
                        })
                        pre_num = pre_num + 1

                if leixing == '电影':
                    play_url = "".join(x.xpath('.//div[@class="result-bottom-pos"]/a/@href'))
                    if play_url.startswith("//"):
                        play_url = 'https://' + play_url[2:]
                    result_list.append(play_url)

                ret["play_list"] = result_list
                print(ret)
                ret_list.append(ret)

        except Exception as e:
            pass

    return ret_list


@app.route("/api/v1/url/<name>", methods=['GET'])
def run_job(name):
    ret_list = search(name)
    return {
        "code": 200,
        "msg": ret_list
    }


if __name__ == '__main__':
    app.run("0.0.0.0", PORT)
