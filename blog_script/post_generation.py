"""Requires slugify."""
#!/usr/bin/env python
import sys
from pathlib import Path
from datetime import datetime, date
from urllib.request import urlopen, URLError
import yaml
from post_templates import BLOG_TEMPLATE, EVENT_TEMPLATE


def validate_url(url):
    """
    Validates a URL by attempting to use it.

    This will not work properly without an internet connection.
    """
    try:
        urlopen(url)
        return True
    except (URLError, ValueError) as error:
        return False


def request_metadata():
    post_type = input("Choose post type (blog or event): ") or "blog"
    if post_type == "blog":
        blog_title = input("Blog post title: ")
        blog_authors = input("Post author's GitHub user ID; separate multiple authors with a comma: ")
    if post_type == "event":
        event_name = input("Event name: ")
        event_url = input("Event URL: ")
        while not validate_url(event_url):
            print("Invalid URL.")
            event_url = input("Event URL: ")
        event_start_date = input("Event start date (e.g. May 13, 2026): ")
        event_end_date = input("Event end date (e.g. May 19, 2026; leave blank if same as start date): ") or event_start_date
        involvement = [{}]  # TODO: Or something?
        while True:
            involvement_types = ["attending", "keynote", "talk", "tutorial", "sprint", "booth", "organizing"]
            involvement_type = input(f"How is the team involved? Enter 'attending', 'keynote', 'talk', 'tutorial', 'sprint', 'booth', or 'organizing': ")
            while involvement_type not in set(involvement_types):
                print("Invalid involvement type.")
                involvement_type = input(f"How is the team involved? Enter 'attending', 'keynote', 'talk', 'tutorial', 'sprint', 'booth', or 'organizing': ")
            team_members = input("Enter GitHub user ID for all team members involved, separated by comma: ")
            involvement_start_date = input(f"Start date of {involvement_type} for {event_name} (e.g. May 14, 2026): ")
            try:  # TODO: Make this validation loopy, and a separate function to call repeatedly.
                datetime.strptime(involvement_start_date, "%B %d, %Y")
            except ValueError:
                print("Invalid date format. Must be 'MonthName DD, YYYY', where 'DD' is a one- or two-digit number, and YYYY is the four-digit year.")
            involvement_end_date = input(f"End date of {involvement_type} for {event_name} (e.g. May 15, 2026; leave blank if same as start date): ") or involvement_start_date
            if involvement_type in ["keynote", "talk", "tutorial"]:
                presentation_title = input("Presentation title: ")
            if involvement_type in ["keynote", "talk", "tutorial", "sprint", "booth"]:
                involvement_url = input(f"{involvement_type} URL (leave blank if unavailable): ") or event_url
                while not validate_url(involvement_url):
                    print("Invalid URL.")
                    involvement_url = input(f"{involvement_type} URL (leave blank if unavailable): ") or event_url
            # TODO: STORE THIS SHIT SOMEHOW SO IT'S NOT OVERWRITTEN IN THE NEXT LOOP
            further_involvement = input("Is the team involved in another way (y/N): ") or "N"
            if further_involvement in ["N", "n", "no"]:
                break

    date = datetime.today().strftime("%B %d, %Y")
    if post_type == "blog":
        metadata = {
            "date": date,
        }
    elif post_type == "event":
        metadata = {
            "date": date,
            "event": {},
            "involvement": [{}],
        }

    if post_type == "blog":
        metadata["title"] = blog_title
        metadata["authors"] = [blog_authors]
        metadata["categories"] = ["buzz"]
    if post_type == "event":
        metadata["title"] = f"We'll be at {event_name}!"
        metadata["authors"] = [team_members]
        metadata["categories"] = ["event"]
        metadata["event"]["name"] = event_name
        metadata["event"]["url"] = event_url
        metadata["event"]["date"] = event_start_date
        metadata["event"]["date"] = event_end_date
        metadata["event"]["description"] = """
        Remove this content and update with event description.

        Description should begin on the line below 'description: |-' with that line left intact."""
        metadata["involvement"][0]["type"] = involvement_type
        metadata["involvement"][0]["team_members"] = [team_members]
        if involvement_type in ["keynote", "talk", "tutorial"]:
            metadata["involvement"][0]["presentation_title"] = presentation_title
        if involvement_type in ["keynote", "talk", "tutorial", "sprint", "booth"]:
            metadata["involvement"][0]["url"] = involvement_url
        metadata["involvement"][0]["date"] = involvement_start_date
        metadata["involvement"][0]["end_date"] = involvement_end_date
        if involvement_type in ["keynote", "talk", "tutorial", "sprint", "booth"]:
            metadata["involvement"][0]["description"] = f"""
            Remove this content and update with {involvement_type} description.

            Description should begin on the line below 'description: |-' with that line left intact."""
        metadata["event"] = {k: metadata["event"][k] for k in
                             ["name", "url", "date", "end_date", "description"] if
                             k in metadata["event"]}
        metadata["involvement"] = [{k: metadata["involvement"][0][k] for k in
                                    ["type", "team_members", "title", "url", "date", "end_date",
                                     "description",] if k in metadata["involvement"][0]}]
    metadata = {k: metadata[k] for k in ["title", "date", "authors", "categories", "event", "involvement"] if k in metadata}
    print(metadata)


def generate_content(metadata):
    date = datetime.strptime(metadata["date"], "%B %d, %Y")
    new_file = "filepath"

    if Path(new_file).is_file():
        print("Post already exists.")
        pass
    else:
        with open(new_file, "w") as w:
            w.write(file_content)
        print("File created -> " + new_file)
    # call(["pycharm", new_file])  # Opens PyCharm. Update to your editor. "open" in macOS. print file path for clicky purposes


if __name__ == "__main__":
    events = {}
    metadata = request_metadata()



# prompt_value = input("The prompt: ")
# event with multiple involvements:
# a template for attending event only
# type: attending
# write this post first.
