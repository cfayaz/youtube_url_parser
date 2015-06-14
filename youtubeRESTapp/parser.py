from lxml import html
import requests
import re

class Parser(object):

    def __init__(self, video_id):
        # Initialize any variables you need from the input you get
        self.video_id=video_id

    def parse_url(self,url):
        rep = {"url=":"","%3A": ":", "%2F": "/","%3F":"?","%3D":"=","%26":"&","%252":"%2"}
        rep = dict((re.escape(k), v) for k, v in rep.iteritems())
        pattern = re.compile("|".join(rep.keys()))
        url = pattern.sub(lambda m: rep[re.escape(m.group(0))], url)
        return url

    def do_parse(self):
        url="https://www.youtube.com/watch?v="+self.video_id
        page = requests.get(url)
        tree = html.fromstring(page.text)
        #Parse the script tag inside div id='player-mole-container'
        script = tree.xpath("//div[@id='player-mole-container']/script[last()]/text()")
        #Parse the title of the video
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
                if item.startswith('url'):
                    urls.append(self.parse_url(item))
                elif item.startswith('itag'):
                    itags.append(item)
        #Creating the response from here
        result=[]
        title_element = {}
        title_element['title'] = title.strip();
        result.append(title_element)
        i = 0
        for itag in itags:
            result_element = {}
            result_element['itag']=itags[i][5:]
            result_element['url'] = urls[i]
            i+=1
            result.append(result_element)
        return result