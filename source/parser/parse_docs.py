import os
import configparser


def get_config(file) -> dict:
    config = configparser.ConfigParser()
    config.read(file)

    names = []
    order = []

    if config.has_option("general", "order"): 
        order = config["general"]["order"].split(" ")

        # Make sure index.md is always prioritized
        if "index.md" in order:
            order.remove("index")
        order.insert(0, "index.md")

    if config.has_section("names"):
        names = {x[0]:x[1] for x in config.items("names")}

    return {"names":names, "order":order}


def get_docs(path, depth=0):
    if depth > 1:
        raise RecursionError("Exceeded max folder depth of 1")

    raw_files:list = os.listdir(path)
    result = []
    config = {"names":{}, "order":["index.md"]}

    # Check if config exists, and if so, load it
    if "nav.cfg" in raw_files:
        config = get_config(path+"/nav.cfg")
        raw_files.remove("nav.cfg")

    files = []
    # Load files from order first
    for file in config["order"]:
        if not file in raw_files:
            print(f"File not found {file}, continuing with order")
            continue
        files.append(file)

    # Load remaining files
    for file in raw_files:
        if file in files: continue
        files.append(file)

    # Get data
    for name in files:
        template = {"name":name.rstrip(".md").title(), "type":"file", "data":None}
        if name in config["names"]:
            template["name"] = config["names"][name]

        target_dir = path+"/"+name
        if os.path.isdir(target_dir):
            template["type"] = "folder"
            template["data"] = get_docs(target_dir, depth+1)
        else:
            with open(target_dir, "r") as f:
                template["data"] = f.read().splitlines()

        result.append(template)
    
    return result
