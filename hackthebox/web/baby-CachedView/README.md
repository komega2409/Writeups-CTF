# baby CachedView
![image](https://user-images.githubusercontent.com/44206101/147847746-88fa977d-8759-43f2-a663-918c2e22153e.png)
## First look
![image](https://user-images.githubusercontent.com/44206101/147847842-acfc7fbb-26b3-4765-8c8f-d18b188b4256.png)

Fill "https://zingnews.vn" (a famous digital magazine in Vietnam) in the URL input
![image](https://user-images.githubusercontent.com/44206101/147847916-986341cc-33ef-4369-93e8-4e7557443d10.png)

In Burp Suite
![image](https://user-images.githubusercontent.com/44206101/147847967-43189c19-77e3-4f79-8e60-002d59a00a8f.png)

A cached view screenshot with filename `3db927a78c5b3e5ca51ae9bfc334.png` is stored. That's it.

This is a `white box` challenge, so we need to audit souce code.

## Audit
*routes.py*
```python
from flask import Blueprint, request, render_template, abort, send_file
from application.util import cache_web, is_from_localhost

web = Blueprint('web', __name__)
api = Blueprint('api', __name__)

@web.route('/')
def index():
    return render_template('index.html')

@api.route('/cache', methods=['POST'])
def cache():
    if not request.is_json or 'url' not in request.json:
        return abort(400)
    
    return cache_web(request.json['url'])

@web.route('/flag')
@is_from_localhost
def flag():
    return send_file('flag.png')
```

Obviously, this part leads us to the flag
```python
@web.route('/flag')
@is_from_localhost
def flag():
    return send_file('flag.png')
```

Now, let's audit `is_from_localhost` function in `util.py`
```python
def is_from_localhost(func):
    @functools.wraps(func)
    def check_ip(*args, **kwargs):
        if request.remote_addr != '127.0.0.1' or request.referrer:
            return abort(403)
        return func(*args, **kwargs)
    return check_ip
```
As sure as daylight, it checks whether the ip address is localhost. If localhost, return the flag.

Try URL: `http://127.0.0.1/flag`. Oops! `IP now allowed`, maybe `127.0.0.1` is inner  blacklist.
![image](https://user-images.githubusercontent.com/44206101/147848114-59ac493b-99a3-48dd-8d93-fecf431f61a6.png)

Yep! There's an ip address filter here
```python
def is_inner_ipaddress(ip):
        ip = ip2long(ip)
        return ip2long('127.0.0.0') >> 24 == ip >> 24 or \
                ip2long('10.0.0.0') >> 24 == ip >> 24 or \
                ip2long('172.16.0.0') >> 20 == ip >> 20 or \
                ip2long('192.168.0.0') >> 16 == ip >> 16 or \
                ip2long('0.0.0.0') >> 24 == ip >> 24
    
if is_inner_ipaddress(socket.gethostbyname(domain)):
        return flash('IP not allowed', 'danger')
```

Now, we think about Server-side request forgery (also known as SSRF) bypass with DNS rebinding.

We can use this tool: https://lock.cmpxchg8b.com/rebinder.html
![image](https://user-images.githubusercontent.com/44206101/147848619-46980bc7-7f5f-4b5f-89c1-753b5ae36ac5.png)

We use 2 ip addresses:
- `127.0.0.1`: localhost
- `8.8.8.8`: Google's DNS

Because the hostname generated (`7f000001.08080808.rbndr.us`) will resolve randomly to one of the addresses specified with a very low ttl, maybe we have to try many times
![image](https://user-images.githubusercontent.com/44206101/147848730-09e8c01b-43db-4455-b10c-0536aed327b1.png)

## Get the flag
Enter URL: `http://7f000001.08080808.rbndr.us/flag` and wait for seconds
![image](https://user-images.githubusercontent.com/44206101/147849154-2cda75fc-cf72-438d-9261-189127464b82.png)

*Note: If you don't get the flag at the first time, don't worry about that. Just keep submitting, the flag is coming to town!*
