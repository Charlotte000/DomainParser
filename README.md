# Domain parser

## How to start
1. Create virtual environment
    ```bash
    python -m venv .venv
    ```
2. Activate *venv*
3. Install required pip packages
    ```bash
    pip install -r .\requirements.txt
    ```
4. Run server
    ```bash
    python manage.py runserver 8000
    ```
---
## How to use
Create *GET* request **localhost:8000** with the following body:
- *url* - **required**
- *limit* - max amount per page
- *page_num* - page number
- *filter* - filter condition
- *sort* - column name

Request example:
```bash
curl -X GET \
-H "Content-type: application/json" \
-H "Accept: application/json" \
-d "{ \
    'url': 'https://google.com', \
    'limit': 10, \
    'page_num': 2, \
    'filter': { 'country': 'RU' }, \
    'sort': 'create_date' \
}" \
"http://localhost:8000"
```

You can also use **localhost:8000?html=true** to get an html table