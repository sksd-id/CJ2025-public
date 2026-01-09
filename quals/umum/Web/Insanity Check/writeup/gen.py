#!/usr/bin/env python3

import itertools
import os

URL = "https://e4ccf83d1f88.ngrok-free.app"

TEMPLATE_START = '''a[href^="/workspace/display/%s"]{--a_%s: url(%s?START=%s);}'''

TEMPLATE_MATCH = '''a[href*="%s"]{--b_%s: url(%s?MATCH=%s);}'''

TEMPLATE_END = ''' a[href$="%s"]{--c_%s: url(%s?END=%s);}'''

TEMPLATE_BACKGROUND_SCRIPT = '''a[href^="/workspace/display/"]{background: %s;}'''

CHARSET = "0123456789abcdef"

CSS_DIR = "static/css"

start_css = ""
end_css = ""
match_css_1 = ""
match_css_2 = ""
match_css_3 = ""

props_start = []
props_end = []
props_match_1 = []
props_match_2 = []
props_match_3 = []

for cs in itertools.product(CHARSET, repeat=2):
    s = "".join(cs)
    start_css += TEMPLATE_START % (s, s, URL, s)
    end_css += TEMPLATE_END % (s, s, URL, s)
    props_start.append(f"var(--a_{s},none)")
    props_end.append(f"var(--c_{s},none)")

for i, cs in enumerate(itertools.product(CHARSET, repeat=3)):
    s = "".join(cs)
    if i <= 3500:
        match_css_1 += TEMPLATE_MATCH % (s, s, URL, s)
        props_match_1.append(f"var(--b_{s},0)")
    elif i <= 7000:
        match_css_2 += TEMPLATE_MATCH % (s, s, URL, s)
        props_match_2.append(f"var(--b_{s},0)")
    elif i <= 10500:
        match_css_3 += TEMPLATE_MATCH % (s, s, URL, s)
        props_match_3.append(f"var(--b_{s},0)")

# create directory if not exists
if not os.path.exists(CSS_DIR):
    os.makedirs(CSS_DIR)

with open(f'{CSS_DIR}/first.css', 'wt') as fp:
    fp.write(start_css)
    fp.write(TEMPLATE_BACKGROUND_SCRIPT % (",".join(props_start)))

with open(f'{CSS_DIR}/second.css', 'wt') as fp:
    fp.write(end_css)
    fp.write(TEMPLATE_BACKGROUND_SCRIPT % (",".join(props_end)))

with open(f'{CSS_DIR}/third.css', 'wt') as fp:
    fp.write(match_css_1)
    fp.write(TEMPLATE_BACKGROUND_SCRIPT % (",".join(props_match_1)))

with open(f'{CSS_DIR}/fourth.css', 'wt') as fp:
    fp.write(match_css_2)
    fp.write(TEMPLATE_BACKGROUND_SCRIPT % (",".join(props_match_2)))

with open(f'{CSS_DIR}/fifth.css', 'wt') as fp:
    fp.write(match_css_3)
    fp.write(TEMPLATE_BACKGROUND_SCRIPT % (",".join(props_match_3)))