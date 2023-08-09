SessionId=None
RequestVerificationToken=None

class ApisHeaders:
    def __init__(self, data = None,type=None):

        headers = {
        
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://student.gehu.ac.in/",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://student.gehu.ac.in",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        }
        if SessionId:
            headers["Cookie"]=f"ASP.NET_SessionId={SessionId}; __RequestVerificationToken={RequestVerificationToken}"
        if data:
            if not type:
                type="application/x-www-form-urlencoded"
            headers["Content-Type"]=type
            headers["Content-Length"]= f"{len(data)}"

        token_head = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Service-Worker-Navigation-Preload": "true",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        if SessionId:
            token_head["Cookie"]=f"ASP.NET_SessionId={SessionId}; __RequestVerificationToken={RequestVerificationToken}"
        self.token_head=token_head
        self.headers = headers