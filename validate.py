"""Validate publishable HTML, routes, supplied copy, metadata and assets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET
from PIL import Image
import build

ROOT = Path(__file__).resolve().parent
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags=[]
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag,dict(attrs)))

count=0
for lang,route in build.ROUTES.items():
    for name in ['index.html','privacy.html']:
        path=ROOT/route/name
        text=path.read_text(encoding='utf-8')
        page=Page(text)
        assert '\ufffd' not in text and '???' not in text, path
        assert [(t,a) for t,a in page.tags if t=='html'][0][1]['lang']==lang
        assert len([1 for t,a in page.tags if t=='h1'])==1
        ids=[a['id'] for t,a in page.tags if 'id' in a]
        assert len(ids)==len(set(ids)), path
        canonical=[a['href'] for t,a in page.tags if t=='link' and a.get('rel')=='canonical']
        expected=build.BASE+route+('privacy.html' if name=='privacy.html' else '')
        assert canonical==[expected],canonical
        alternate=[a for t,a in page.tags if t=='link' and a.get('rel')=='alternate']
        assert {a['hreflang'] for a in alternate}=={'en','it','ru','x-default'}
        for t,a in page.tags:
            for key in ['href','src']:
                if key not in a: continue
                u=urlsplit(a[key])
                if u.scheme in ['https','mailto']: continue
                assert not u.scheme,a
                target=(path.parent/unquote(u.path)).resolve() if u.path else path
                if target.is_dir(): target=target/'index.html'
                assert target.is_file(),(path,a[key],target)
                if u.fragment:
                    target_ids=[b.get('id') for _,b in Page(target.read_text(encoding='utf-8')).tags]
                    assert u.fragment in target_ids,(path,a[key])
            if t=='img':
                assert a.get('alt') and a.get('width') and a.get('height')
            assert t not in ['iframe','form'],(path,t)
            if t=='script': assert a.get('type')=='application/ld+json' and 'src' not in a
        if name=='index.html':
            import re
            for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text):
                graph=json.loads(raw)
                assert len(graph['@graph'])==3
                assert not any(k in raw for k in ['AggregateRating','aggregateRating','reviewRating'])
            for value in ['€225','€270','€298','€140','€155','€30','€33','€160','€176','€370','€400','Europe/Rome','Azra','Carolina','Corinne']:
                assert value in text,(lang,value)
            for group in ['hero','about','approach','individual','group','call','app']:
                for paragraph in build.DATA[lang][group]:
                    assert build.e(paragraph) in text,(lang,group)
            for tag,a in page.tags:
                if tag=='a' and a.get('class')=='button':
                    assert a['href'].startswith('mailto:grammilla.academy@gmail.com?subject=')
            assert '04015341201' in text
        count+=1
root=ET.parse(ROOT/'sitemap.xml').getroot()
assert len(root)==6
for size in [540,1080]:
    assert Image.open(ROOT/'assets'/f'liuba-{size}.webp').size==(size,size)
assert Image.open(ROOT/'assets'/'social.jpg').size==(1200,630)
titles=[d['title'] for d in build.DATA.values()]
assert len(set(titles))==3
print(f'PASS: {count} UTF-8 pages; local files/anchors; language routes; canonical/hreflang; JSON-LD; exact author paragraphs; confirmed prices; mailto; images and sitemap.')
