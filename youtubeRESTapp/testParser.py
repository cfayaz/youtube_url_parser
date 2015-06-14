from lxml import html
import requests
import re

class Parser(object):

    def __init__(self, *args, **kw):
        # Initialize any variables you need from the input you get
        pass

    def parse_url(self,url):
        rep = {"url=":"","%3A": ":", "%2F": "/","%3F":"?","%3D":"=","%26":"&","%252":"%2"}
        rep = dict((re.escape(k), v) for k, v in rep.iteritems())
        pattern = re.compile("|".join(rep.keys()))
        url = pattern.sub(lambda m: rep[re.escape(m.group(0))], url)
        return url

    def do_parse(self):
        f = open('debug_url.txt','w')
        f2 = open('debug_url_raw.txt','w')
        f3 = open('script_raw.txt','w')
        url="https://www.youtube.com/watch?v=NkgAl8cbzyM"
        #url = "https://www.youtube.com/watch?v=UAElM3oymd0"
        page = requests.get(url)
        tree = html.fromstring(page.text)
        #Parse the script tag inside div[@id='player-mole-container'
        script = tree.xpath("//div[@id='player-mole-container']/script[last()]/text()")  
        f3.write(script[0])
        #Parse title of video
        m = re.search(r'(\"title\")(:")(?P<title>.*?)(\",\")', script[0])
        if m:
            print m.group('title')
            title = m.group('title')
        else:
            print 'no result'
        #Parse the base url collection
        m = re.search(r'(\"url_encoded_fmt_stream_map\")(:")(?P<url>.*?)(\",\")', script[0])
        if m:
            base_url = m.group('url')
        else:
            print 'no result'
        #base_url = base_url.split('\u0026')
        base_url = re.split('(\\\\u0026)|(,)',base_url)
        print base_url
        itags = []
        urls = []

        for item in base_url:

            if item:
                f2.write(item)
                if item.startswith('url'):
                    urls.append(self.parse_url(item))
                elif item.startswith('itag'):
                    itags.append(item)                     

        print itags
        print urls
        for item in urls:
            f.write("%s\n" % item)    
        f.close() 
        f2.close()
        f3.close()
        result = ((1,2,3, ), (4,5,6,))
        return result

myParser = Parser('abc', 'def', [], [])
result = myParser.do_parse()
print result