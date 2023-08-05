import requests

class Itsperfect:
    """ITSPerfect integration requests"""

    def __init__(self, url, token, version="v2"):
        self.url = url
        self.token = token
        self.version = version

    def setFullUrl(self, category, objectId="", subject="", requestFilter=""):
        """Build url for requests"""

        if objectId != "":
            objectId = f"/{objectId}"

        if subject != "":
            subject = f"/{subject}"

        if requestFilter != "":
            requestFilter = f"&filter={requestFilter}"

        url = f"https://{self.url}/api/{self.version}/{category}{objectId}{subject}"
        url = f"{url}/&token={self.token}{requestFilter}"

        return url

    def getOne(self, keyName, objectId, subject="", requestFilter=""):
        """Get one for any itsp route"""
        result = []
        fullUrl = self.setFullUrl(keyName, objectId, subject, requestFilter)

        if subject != "":
            keyName = subject

        response = requests.get(fullUrl)
        if response.status_code == 200:
            pageItems = response.json()[keyName]
            result.extend(pageItems)
        else:
            # Handle unsuccessful API response
            print(f"Failed to fetch data from URL: {fullUrl}")
        return result

    def getAll(self, keyname):
        """Get many for any itsp route"""
        print("Get all", keyname)
        return ""
