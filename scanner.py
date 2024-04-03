import requests

def populateHeaders():
    domainsFile = open("domains.txt", "r")
    for domain in domainsFile:
        domainClean = f"http://{domain.strip()}/"
        print(f"Using domain: {domainClean}")
        try:
            result = requests.head(domainClean, allow_redirects=True, timeout=2)
            print(result.headers)
        except requests.exceptions.Timeout:
            print("Timeout")
            continue
        except requests.exceptions.ConnectionError:
            print("Connection error")
            continue


def main():
    populateHeaders()

if __name__ == "__main__":
    main()