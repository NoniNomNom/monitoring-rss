import json
import pandas as pd
from pathlib import Path

path = Path(__file__)
app_dir = path.parent.absolute()
print(app_dir)
app_dir = str(app_dir)

feeds_dict = {}

feeds_dict["feed_title"] = []

feeds_dict["feed_url"] = []

def make_feed_dict():
    feeds = json.dumps(feeds_dict)
    with open(app_dir + "/feeds_dict.json", "w") as outfile:
        outfile.write(feeds)
    print("FILE WRITTEN")

    
def make_selected_dict():
    feeds = json.dumps(feeds_dict["feed_title"])
    with open(app_dir + "/feeds_selected.json", "w") as outfile:
        outfile.write(feeds)
    print("FILE WRITTEN")

keywords = []

def make_keywords_list():
    list = json.dumps(keywords)
    with open(app_dir + "/keywords.json", "w") as outfile:
        outfile.write(list)
    print("FILE WRITTEN")

def make_all_data():
    df = pd.DataFrame({"Title":{},"Date":{},"Day":{},"Month":{},"Year":{},"Hour":{},"URL":{},"Description_all":{},"Description":{},"Feed":{}})
    df.to_json("all_data.json")

def make_kept_rows():
    df = pd.DataFrame({"Title":{},"Date":{},"Day":{},"Month":{},"Year":{},"Hour":{},"URL":{},"Description_all":{},"Description":{},"Feed":{}})
    df.to_json("kept_rows.json")

# make_feed_dict()
# make_selected_dict()
# make_keywords_list()
# make_all_data()
# make_kept_rows()