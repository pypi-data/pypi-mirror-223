import requests

url = "https://api.github.com/repos/tauri-apps/tauri-action/releases?per_page=&page="
url = "https://api.github.com/repos/lijc210/woo-app/releases?per_page=&page="
url = "https://api.github.com/repos/lijc210/woo-app/releases/latest"

payload = {}
headers = {
    "Authorization": "token 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",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json",
}
login = requests.get("https://api.github.com/user", headers=headers)


response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)

res_dict = response.json()
assets = res_dict["assets"]
