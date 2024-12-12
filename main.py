from outline_vpn_api_client import OutlineClient

def main():
    client = OutlineClient("https://146.185.218.101:41023/wH9tEDXAA-LY0qW8FQHyPA")
    client.access_keys.create_with_special_id(0, "special_key")

if __name__ == "__main__":
    main()