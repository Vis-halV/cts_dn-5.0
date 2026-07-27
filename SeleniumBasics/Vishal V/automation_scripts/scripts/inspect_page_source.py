import requests

url = 'https://www.lambdatest.com/selenium-playground/simple-form-demo'
html = requests.get(url, timeout=20).text
print(html[:5000])
print('---MATCHES---')
for pat in ['showInput', 'message', 'getCheckedValue', 'onclick', 'addEventListener', 'js']:
    print(pat, html.lower().count(pat.lower()))
