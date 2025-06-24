import os
import configparser
from source.parser.mdparser import parse_data
from source.parser.parse_docs import get_docs
from source.parser.webgen import generate_website

directory = os.path.dirname(os.path.abspath(__file__))

config = configparser.ConfigParser()
config.read('settings.cfg')

if not config.has_option("general", "title"):
    raise IndexError("Index 'title' under section 'general' not specified in settings.ini")

# Load title
title = config.get("general", "title")

# Load theme
theme = "dark"

if config.has_option("general", "theme"):
    theme = config.get("general", "theme")

target_folder = "docs"
if config.has_option("general", "folder"):
    target_folder = config.get("general", "folder")

docs_data = get_docs(directory + "/" + target_folder)

result = parse_data(docs_data)
html = generate_website(theme, title, result, directory)

if len(html) > 160_000:
    print("\x1b[31m##############################################################")
    print("\x1b[31m# WARNING: Content exceeds 160k character limit for greyhack #")
    print("\x1b[31m##############################################################\x1b[0m")

with open(directory+"/result/"+target_folder+".html", "w") as f:
    f.write(html)

print(f"\x1b[32mContent saved to {target_folder}.html\x1b[0m\n\n\n")
input("\x1b[90mPress enter to continue. . .\x1b[0m")