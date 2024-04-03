import requests, warnings

warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

securityHeaders = ["Content-Security-Policy",
                   "Permissions-Policy",
                   "Strict-Transport-Security",
                   "X-Content-Type-Options"]

def populateHeaders():
    domainsFile = open("domains.txt", "r")
    domainHeaderDict = {}
    for domain in domainsFile:
        domainClean = f"https://{domain.strip()}/"
        try:
            result = requests.head(domainClean, allow_redirects=True, timeout=2, verify=False)
            domainHeaderDict[domainClean] = dict(result.headers)
        except requests.exceptions.Timeout:
            continue
        except requests.exceptions.ConnectionError:
            continue
    return domainHeaderDict

def checkHeaders(domainHeaderDict):
    result = {}
    for header in securityHeaders:
        lowerCaseHeader = header.lower()
        result[header] = []
        for domain in domainHeaderDict:
            lowerDomainHeaderDict = {key.lower(): value for key, value in domainHeaderDict[domain].items()}
            if lowerCaseHeader not in lowerDomainHeaderDict:
                result[header].append(domain)
    return result


def main():
    domainHeaderDict = populateHeaders()
    result = checkHeaders(domainHeaderDict)
    for header, domains in result.items():
        print(header)
        print(domains)

if __name__ == "__main__":
    main()