from django.shortcuts import render, HttpResponse

from bs4 import BeautifulSoup
import requests
import json
from django.http import JsonResponse
import yt_dlp as youtube_dl
import re

from .yt_scrapper import *


def home(request):
    if request.method == "GET":
        query = request.GET.get('q', None)
        
        videos = get_videos(query)
            
    context = {"videos":videos}

    if len(videos) == 1:
        print("Videos: ", videos[0].keys())
        video_url = f'https://www.youtube.com/watch?v={videos[0]["id"]}'
        context = get_download_links(video_url=video_url)
        return render(request, "home/download.html", context)

    return render(request, "home/home.html", context)

def home_scraper(request):

    driver = get_all_videos()
    soup = scroll(driver,5)
    context = {'video_ids': get_next_page(driver)}
    return render(request, "home/home_scrape.html", context=context)


def get_videos(query):
    base = "https://www.genyt.com/search.php?q="
    if not query:
        query = "therui"
    response = requests.get(base+query)

    videos = []

    if response.status_code == 200:

        soup = BeautifulSoup(response.content, 'html.parser')
        containers = soup.find_all('div', {'class' :'col-12 mb-3'})

        try:
            for container in containers:
                video = {}
                video['id'] = container.find('a').attrs['href'].split('/')[-1]
                video['thumbnail_attrs'] = container.find('img').attrs
                video['duration'] = container.find('span', {'class': 'duration'}).text
                video['title'] = container.find('h5', {'class': 'gytTitle'}).text
                video['user'] = container.find('small', {'class': 'd-block text-truncate'}).find('a').text
                date_views = container.find('small', {'class': 'd-block text-truncate'}).find('span', {"class":"d-n-450"}).text.split()
                
                date_views = container.find('small', {'class': 'd-block text-truncate'}).find('span', {"class":"d-n-450"}).text.split()

                if 'views' in date_views:
                    video['views'] = date_views[1]
                else:
                    video['views'] = 0

                if 'ago' in date_views:
                    video['upload_date'] = date_views[4] +' '+ date_views[5]
                else:
                    video['upload_date'] = ''
                    
                videos.append(video)
        except Exception as e:
            print("Error: "+str(e)+'. ',len(videos))

    return videos





def download(request, id):
    
    video_url = f'https://www.youtube.com/watch?v={id}'

    regex = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
    #regex = (r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$\n")
    print(video_url)
    
    if not re.match(regex,video_url):
        print('Invalid Url')
        return HttpResponse('Enter correct url.')

    context = get_download_links(video_url)
    return render(request, 'home/download.html', context)


def get_download_links(video_url):
    video_id = video_url.split('=')[1]

    ydl_opts = {}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            meta = ydl.extract_info(
                video_url, download=False)
        except:
            context = {'video_id': video_id}
            return context

    video_audio_streams = []
    for m in meta['formats']:
        resolution = 'Audio'
        if m['height'] is not None:
            resolution = f"{m['height']}x{m['width']}"
        video_audio_streams.append({
            'resolution': resolution,
            'extension': m['ext'],
            'video_url': m['url'],
            'acodec':m['acodec'],
            'vcodec':m['vcodec'],
            
        })
    # reverse the list
    video_audio_streams = video_audio_streams[::-1]

    context = {
        'meta': meta.keys(),
        'video_id': video_id,
        'title': meta['title'], 'streams': video_audio_streams,
        'description': meta['description'], 
        'duration': round(int(meta['duration'])/60, 2), 'views': f'{int(meta["view_count"]):,}',
    }

    return context

