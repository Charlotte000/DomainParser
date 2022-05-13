import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from domainparser.parser import get_data


def index(request: WSGIRequest):
    if request.method == 'GET':
        # Get body data
        body: dict = json.loads(request.body.decode('utf-8').replace("'", '"')) if request.body != b'' else {}
        if 'url' not in body:
            if 'url' not in request.GET:
                return HttpResponse('{ "status": "url not found"}', content_type="application/json", status=404)

            body['url'] = request.GET['url']
        
        if not body['url'].startswith('http'):
            body['url'] = 'http://' + body['url']

        limit: int = max(1, body.get('limit', 9999))
        page_num: int = max(1, body.get('page_num', 1))
        filtration: dict = body.get('filter', {})
        sorting: str = body.get('sort', None)

        # Get required data
        result: list[dict] = get_data(body['url'], limit, page_num, filtration, sorting)

        if request.GET.get('html', 'false') == 'true':
            return render(request, 'view.html', context={'data': result})
        
        return HttpResponse(json.dumps({ 'status': 'ok', 'data': result }), content_type="application/json")
