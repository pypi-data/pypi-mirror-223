# Custom apiclient

[dbutils](https://github.com/gonzalo123/apiclient)

## Install

```commandline
pip install apiclient-gonzalo123
```

## Usage

Init client
```python
from apiclient import ApiClient

client = ApiClient(token='my_secret token', base='http://localhost:8000')
```

GET Request
```python
data = client.get('/api/route', dict(param1='value1'))
```

POST Request (with parameters in the url)
```pythonº
data = client.post('/api/route', params=dict(param1='value1'))
```

POST Request (with parameters in the request body)
```python
data = client.post('/api/route', body=dict(param1='value1'))
```