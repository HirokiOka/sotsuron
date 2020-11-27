import os
from urllib import request as req
from urllib import error
from urllib import parse
import bs4
from PIL import Image

def google_search(keyword):

    urlKeyword = parse.quote(keyword)
    url = 'https://www.google.com/search?hl=jp&q=' + urlKeyword + '&btnG=Google+Search&tbs=0&safe=off&tbm=isch'

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",}
    request = req.Request(url=url, headers=headers)
    page = req.urlopen(request)

    html = page.read().decode('utf-8')
    html = bs4.BeautifulSoup(html, "html.parser")
    elems = html.select('.rg_meta.notranslate')
    ele = elems[0]
    ele = ele.contents[0].replace('"','').split(',')
    eledict = dict()
    for e in ele:
        num = e.find(':')
        eledict[e[0:num]] = e[num+1:]
    imageURL = eledict['ou']

    pal = '.jpg'
    # if '.jpg' in imageURL:
    #     pal = '.jpg'
    # elif '.JPG' in imageURL:
    #     pal = '.jpg'
    # elif '.png' in imageURL:
    #     pal = '.png'
    # elif '.gif' in imageURL:
    #     pal = '.gif'
    # elif '.jpeg' in imageURL:
    #     pal = '.jpeg'
    # else:
    #     pal = '.jpg'

    try:
        img = req.urlopen(imageURL)
        localfile = open("/Users/Hiroki/Documents/Processing/prototype5/data/google_image"+pal, 'wb')
        localfile.write(img.read())
        img.close()
        localfile.close()
        return ("google_image" + pal)

    except UnicodeEncodeError:
        pass
    except error.HTTPError:
        pass
    except error.URLError:
        pass
