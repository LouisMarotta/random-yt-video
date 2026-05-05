from random import choice
import webbrowser
import argparse
import feedparser
import requests


def main(channel_name: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    response = requests.get(f'https://inv.thepixora.com/api/v1/search?q=@{channel_name}&type=channel', headers=headers);
    channels_info = response.json()

    if len(channels_info) <= 0:
        raise Exception("Channel not found")

    channel_info = channels_info[0]

    if channel_info['authorId']:
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_info['authorId']}"
    else:
        raise Exception("Channel not found")
    
    channel_data = feedparser.parse(url)
    if not channel_data.entries:
        raise Exception("No videos available")

    video = choice(channel_data.entries)
    webbrowser.open(video.link)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Random Youtube Video')
    parser.add_argument('-c', '--channel',  help='Youtube channel', type=str)

    args = parser.parse_args()

    if not args.channel:
        raise Exception("Channel required")
    
    channel_name = args.channel
    main(channel_name)
