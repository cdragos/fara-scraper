from pathlib import Path

from scrapy.http import Request, HtmlResponse


def fake_response(filename, url, meta={}):
    request = Request(url=url)
    request.meta.update(meta)
    filepath = Path(__file__).parent / Path(filename)

    content = ''
    if filepath.is_file():
        with filepath.open('r') as f:
            content = f.read()

    return HtmlResponse(url=url, request=request, body=content, encoding='utf-8')
