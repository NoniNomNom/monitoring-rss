from shiny import ui
from datetime import datetime, timedelta
import re
import feedparser
import json
import pandas as pd


def get_json_content(file_name):
    with open(file_name, "r") as f: 
            f = json.load(f)
    content = f
    return content

def parse_and_append(feed_url, feed_name, all_data = None, error = 0, out_time = 0):

        parsed_feed = feedparser.parse(feed_url)
        parsed_entries = []
   
        back = datetime.now() - timedelta(days=30) # changer le nombre de jours si besoin
        
        entries = parsed_feed.entries if 'entries' in parsed_feed else []
        print(len(entries))
        
        for entry in entries:
            title = entry.title

            if not title:
                print("NO TITLE")
                error = error + 1
                continue
            else :
                date = entry.published_parsed if 'published_parsed' in entry else None
                if date and datetime(*date[:6]) < back or date is None:
                    print("OUT OF TIME")
                    out_time = out_time + 1
                    continue
                url = entry.link if 'link' in entry else None
                description = entry.summary if 'summary' in entry else None
                words = re.sub('<[^<]+?>', '', description)
                words = str(words).split()
                description_short = ' '.join(words[:15])
                formatted_date = datetime.strftime(datetime(*date[:6]), "%d-%m-%Y - %H:%M") if date else None
                formatted_day = datetime.strftime(datetime(*date[:6]), "%d") if date else None
                formatted_month = datetime.strftime(datetime(*date[:6]), "%m") if date else None
                formatted_year = datetime.strftime(datetime(*date[:6]), "%Y") if date else None
                formatted_hour = datetime.strftime(datetime(*date[:6]), "%H:%M") if date else None

                print(formatted_date)
                
                formatted_date = str(formatted_date)

                parsed_entries.append({
                    "Title": title,
                    "Date": formatted_date,
                    "Day": int(formatted_day),
                    "Month": int(formatted_month),
                    "Year": int(formatted_year),
                    "Hour": formatted_hour,
                    "URL": url,
                    "Description_all": description,
                    "Description": description_short,
                    "Feed": feed_name,
                })

        return parsed_entries, parsed_feed

def load_feeds(nloads = 0):

    try:
        content = get_json_content("all_data.json")
        all_data = pd.DataFrame(content)

    except Exception as e:
        print(e)
        all_data = None
        print("no df")

    feeds = get_json_content("feeds_dict.json")

    df_feeds = pd.DataFrame(feeds)
    parsed_table = []
    error = 0
    out_time = 0
    feed_broken = 0
    feeds_broken = []

    ui.notification_show("Parsing feeds", 
                        duration=120, 
                        type="message",
                        id="id_parsing"+str(nloads))

    for index, row in df_feeds.iterrows():
        feed_url = row['feed_url']
        feed_name = row['feed_title']
        print(feed_name)
        try:
            parsed_entries, parsed_feed = parse_and_append(feed_url, feed_name, all_data)
            parsed_table.extend(parsed_entries)
        except Exception as e:
            print(e)
            feed_broken = feed_broken + 1
            feeds_broken.append(feed_name)
            continue

    final_df = pd.DataFrame(parsed_table)

    print(final_df)
    print("NUMBER OF ERRORS:")
    print(error)
    print("NUMBER OF OUT_TIME:")
    print(out_time)
    print("FEEDS BROKEN:")
    print(feed_broken)
    print(feeds_broken)

    final_df.to_json("all_data.json",
                      orient="records")
    
    ui.notification_remove(id="id_parsing"+str(nloads))

    return final_df