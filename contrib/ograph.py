from lxml import html
import requests

response = requests.get('http://www.spiegel.de/politik/deutschland/merkel-fordert-von-mursi-einhaltung-der-menschenrechte-a-880555.html')
document = html.fromstring(response.content)

for meta in document.findall('.//meta'):
    (p, v) = meta.attrib.get('property'), meta.attrib.get('content')
    if p is not None and p.startswith('og:'):
        p = p[3:]
        print (p, v)


