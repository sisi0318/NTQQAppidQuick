import json
import os
import sys
from time import sleep
import frida
import requests

def send_key(msg):
    env = dict(os.environ)
    api = os.getenv('API')
    key = os.getenv('SEND_KEY')
    group = os.getenv('SEND')
    
    if not api or not key or not group:
        raise ValueError("API, SEND_KEY, and SEND environment variables must be set")
    
    data = json.dumps({
        'group_id': group,
        'message': "action appid\n"+msg
    })
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer "+ key
    }
    r = requests.post(api+"/send_group_msg", headers=headers, data=data)

def on_message(message, data):
    if message['type'] == 'send':
        url = os.getenv('QQURL')
        array ="[URL] "+ url + "\n[Appid] "+ str(message['payload'])

        send_key(array)
        print("[Python] [Appid]", message['payload'])

def main():
    # 获取传入的参数
    qq_url = sys.argv[1]
    send_group = sys.argv[2]

    # 设置环境变量
    os.environ['QQURL'] = qq_url
    os.environ['SEND'] = send_group

    env = dict(os.environ)
    pid = frida.spawn(['/opt/QQ/qq', '--no-sandbox'], env=env)
    print("real PID", pid)
    send_key(str(pid))

    session = frida.attach(pid)
    frida.resume(pid)
    with open("GetAppid.js") as f:
        script = session.create_script(f.read())
        script.on('message', on_message)
        script.load()

    print("[!] Ctrl+D on UNIX, Ctrl+Z on Windows/cmd.exe to detach from instrumented program.\n\n")
    sleep(30)
    session.detach()

if __name__ == '__main__':
    main()