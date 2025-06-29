from typing import List
from html import escape as html
# Classes

# Util funcs #
def remove_spaces(text:str):
    return " ".join([x for x in text.split(" ") if x])

def lcount(text:str, char:str):
    return len(text) - len(text.lstrip(char))

widgets = {
    "===":"note",
    "???":"warning",
    "!!!":"important"
}

# Handlers

registered = {}

def register(type):
    if not type in registered:
        registered[type] = 0
    registered[type] += 1
    return registered[type]

handlers = []

@handlers.append
def header(line:str, content:List[str], offset:int):
    if not line.startswith("#"): return
    level = lcount(line, "#")
    if level > 4: return
    title = html(line.lstrip("#").strip())
    tag = "h"+str(level)
    header_id = ""
    if level != 4: header_id = register("header")

    return {
        "type":"header",
        "level":level,
        "header_id":header_id,
        "name":title,
        "format":f'<{tag} id="h_{header_id}">{title}</{tag}></br>',
        "offset": offset + 1
    }


@handlers.append
def code(line:str, content:List[str], offset:int):
    if not line.startswith("```"): return
    title = line.strip("`")
    code_content = []
    for x in content[offset+1:]:
        offset += 1
        if x.startswith("```"): break
        code_content.append(x)
    
    code_content = html("\n".join(code_content))
    title = html(title)

    return {
        "type": "code",
        "format":f'<div class="code"><p>{title}</p><div>{code_content}</div></div>',
        "offset": offset + 1
    }


@handlers.append
def widget(line:str, content:List[str], offset:int):
    if not line[:3] in widgets: return
    widget_type = widgets[line[:3]]
    title = line[3:].strip()
    if title == "": title = widget_type.title()

    widget_content = []
    for x in content[offset+1:]:
        if lcount(x, " ") == 0:
            break

        offset += 1
        if x.strip() == "":
            if widget_content == []: continue
            if widget_content[-1] == "<br/>": continue
            widget_content.append("<br/>")
            continue

        widget_content.append(html(x.strip()))

    if widget_content == []: return
    if widget_content[-1] == "<br/>": widget_content.pop()
    message = " ".join(widget_content)
    icon = line[0]
    if widget_type == "note":
        icon = ":"

    return {
        "type":"widget",
        "format":f'<div class="widget {widget_type}"><div><b>{icon}</b> {title}</div>{message}</div>',
        "offset":offset + 1
    }


@handlers.append
def seperator(line:str, content:List[str], offset:int):
    line = line.strip()
    if line.count("_") != len(line) or len(line) <= 2: return
    return {
        "type":"line",
        "format": '<div class="line"></div>',
        "offset": offset+1
    }


@handlers.append
def array(line:str, content:List[str], offset:int):
    if not line.startswith("-"): return
    data = []
    for x in content[offset:]:
        if not x.startswith("-"): break
        offset += 1
        data.append("<div class=\"list\">"+x[1:].strip()+"</div>")
    data = "".join(data)

    return {
        "type":"list",
        "format":data,
        "offset": offset + 1
    }


@handlers.append
def dropdown(line:str, content:List[str], offset:int):
    if not line.startswith("vvv") and not line.startswith("^^^"): return
    fmt = "</div>"
    drop_type = "close"

    if line.startswith("vvv"):
        drop_type = "open"
        dropdown_id = register("dropdown")
        title = line[4:].strip().split(" ")
        content_classlist = "dropdown hidden"
        button_classlist = "dropdown_close"

        # Dropdown needs title, so check if it's empty
        if title == []: 
            print(f"\x1b[31mNo title for dropown at line {offset+1}. Ignoring dropdown\x1b[0m")
            return

        # Check if default should be open or closed, and remove data from title if so
        if title[-1] == "open" or title[-1] == "closed":
            status = title.pop()
            # remove "closed" but only actually handle things for open
            if status == "open":
                content_classlist = "dropdown"
                button_classlist = "dropdown_open"

        title = " ".join(title)
        fmt = f'<p class="{button_classlist}" id="db_{dropdown_id}">{title}</p><div class="{content_classlist}" id="d_{dropdown_id}">'

    # Register dropdown type count, so we can check if they were closed properly later
    register("dropdown_" +drop_type)

    return {
        "type":"dropdown",
        "dropdown-type": drop_type,
        "format":fmt,
        "offset":offset+1
    }


def get_parsed(line:str, content:List[str], offset:int):
    for h in handlers:
        result = h(line, content, offset)
        if result != None: return result

# Parser

def parse_data(data, depth=0):
    if depth > 1:
        raise RecursionError("\x1b[31mCrowdocs has a maximum depth of 1 folder\x1b[0m")

    pages = []
    for x in data:
        if x["type"] == "folder": 
            print(f"\x1b[90mParsing folder {x['name']}\x1b[0m")
            collection = {
                "type":"collection",
                "name":x["name"],
                "pages": parse_data(x["data"], depth+1)
            }
            print(f"\x1b[90mFinished folder {x['name']}\x1b[0m")
            pages.append(collection)
            continue

        print(f"\x1b[32m{x['name']}\x1b[0m")
        page = {
            "type":"page",
            "name":x["name"],
            "content":[]
        }

        parargaph = {
            "type":"paragraph",
            "content":[],
            "format": None
        }

        index = 0
        while index < len(x["data"]):
            line:str = x['data'][index]
            parsed = get_parsed(line, x["data"], index)

            if parsed != None and parargaph["content"] != []:
                parargaph["format"] = "<p>" + " ".join(parargaph["content"]) + "</p>"
                page["content"].append(parargaph)
                # reset paragraph for next one
                parargaph = {
                    "type":"paragraph",
                    "content":[],
                    "format": None
                }

            if parsed != None:
                index = parsed["offset"]
                page["content"].append(parsed)

            else:
                index += 1

                if line.strip() == "":
                    if parargaph["content"] == []: continue
                    if parargaph["content"][-1] == "<br/>": continue
                    parargaph["content"].append("<br/>")
                else:
                    parargaph["content"].append(line)

        if parargaph["content"] != []:
            parargaph["format"] = "<p>"+" ".join(parargaph["content"])+"</p>"
            page["content"].append(parargaph)
        
        # Check if all dropdowns are closed
        if "dropdown" in registered:
            closed = 0
            opened = registered["dropdown_open"]
            if "dropdown_close" in registered: 
                closed = registered["dropdown_close"]

            if closed != opened:
                raise SyntaxError("\x1b[31mDropdown never closed\x1b[0m")

        pages.append(page)

    return pages