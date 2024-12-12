import json
import os
import re
import subprocess

from outline_vpn_api_client import OutlineClient

def do_ssh_request(host, command):
    try:
        result = subprocess.run(
            ["ssh", "-i", "~/.ssh/id_rsa", host, command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        # Вывод команды
        output = result.stdout
        return output
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        print(f"Стандартный вывод: {e.stdout}")
        print(f"Стандартная ошибка: {e.stderr}")

def set_environment(api_url):
    client = OutlineClient(api_url)
    info = client.server.get_information()
    os.environ["OUTLINE_URL"] = api_url
    os.environ["OUTLINE_SERVER_ID"] = info['serverId']
    os.environ["OUTLINE_DEFAULT_PORT"] = str(info['portForNewAccessKeys'])

def find_api_url(output):
    match = re.search(r'\{.*?\}', output)
    if match:
        json_part = match.group(0)
        # Парсим JSON
        data = json.loads(json_part)
        api_url = data.get("apiUrl")
        if api_url:
            return api_url
        else:
            print("apiUrl не найден в JSON.")
    else:
        print("JSON-строка не найдена в выводе команды.")