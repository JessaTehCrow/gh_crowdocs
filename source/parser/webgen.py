from typing import List

def remove_js_comments(text:List[str]):
    result = []
    for x in text:
        x = x.strip()
        if "//" in x:
            x = x[:x.index("//")]

        # add and remove extra useless spaces
        result.append(x.replace(" = ", "=").replace(") {", "){").replace(", ", ","))

    return "".join(result)

def remove_css_comments(text:List[str]):
    result = []
    for x in text:
        x = x.strip()
        if x.strip().startswith("/*"): continue

        # add and remove extra useless spaces
        result.append(x.replace(": ", ":").replace(" {", "{"))
    return "".join(result)

def remove_leading_spaces(text:str):
    return "\n".join([x.lstrip() for x in text.split("\n")])


def load_data(theme, root_path):
    with open(f"{root_path}/source/themes/{theme}.css") as f:
        theme_css = remove_css_comments(f.readlines())
    
    with open(f"{root_path}/source/webdocs/main.css") as f:
        main_css = remove_css_comments((f.readlines()))
    
    with open(f"{root_path}/source/webdocs/main.js") as f:
        js = remove_js_comments(f.read().splitlines())

    with open(f"{root_path}/source/webdocs/main.html") as f:
        html = remove_leading_spaces(f.read()).replace("\n", "")
    
    return [theme_css + main_css, js, html]


def get_includes(pagecount, page):
    includes = f'<div id="ic_{pagecount}" class="hidden">'

    subs = ""

    for x in page["content"]:
        if x["type"] != "header": continue
        
        if x["level"] < 3 and subs != "":
            includes += subs + "</details>"
            subs = ""
        
        if x["level"] == 1:
            includes += f"<summary id=\"i_{x['header_id']}\" class=\"selected\">{x['name']}</summary>"

        elif x["level"] == 2:
            subs = f"<details><summary id=\"i_{x['header_id']}\">{x['name']}</summary>"
        
        elif x["level"] == 3:
            if subs == "":
                includes += f"<summary id=\"i_{x['header_id']}\">{x['name']}</summary>"
            else:
                subs += f"<p id=\"i_{x['header_id']}\">- {x['name']}</p>"

    if subs != "":
        includes += subs + "</details>"
    includes += "</div>"

    return includes


def generate_website(theme, title, data, root_path):
    css, js, html = load_data(theme, root_path)

    html = html.replace("&&STYLE&&", f"<style>{css}</style>")
    html = html.replace("&&JAVASCRIPT&&", js)
    html = html.replace("&&TITLE&&", title)

    navbar = ""
    include = ""
    page_count = 0
    content = ""

    for x in data:
        if x["type"] == "collection":
            if len(x["pages"]) == 0: continue
            index = True
            for page in x["pages"]:
                page_count += 1
                include += get_includes(page_count, page)
                content += f'<div id="c_{page_count}" class="hidden">' + "".join([y["format"] for y in page["content"]]) + "</div>"
                if index:
                    navbar += f'<details><summary id="n_{page_count}">{x["name"]}</summary>'
                    index = False
                else:
                    navbar += f"<p id=\"n_{page_count}\">- {page['name']}</p>"
            navbar += "</details>"

        else:
            page_count += 1
            content += f'<div id="c_{page_count}" class="hidden">' + "".join([y["format"] for y in x["content"]]) + "</div>"
            include += get_includes(page_count, x)
            navbar += f'<details><summary id="n_{page_count}">{x["name"]}</summary></details>'
    
    html = html.replace("&&NAVBAR&&", navbar)
    html = html.replace("&&INCLUDEBAR&&", include)
    html = html.replace("&&CONTENT&&", content)

    return html