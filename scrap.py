import requests
from bs4 import BeautifulSoup
import re

music_quality = ['128', '320']
video_quality = ['144', '240', '360', '480', '720', '1080']


class DownloderExceptions(Exception):
    pass


class ExistError(DownloderExceptions):
    pass


class QualityError(DownloderExceptions):
    pass


class Scraper:
    def __init__(self, url, quality):
        self.url = url
        self.quality = str(quality)
        self.music_or_video = None

    def get_all_links(self):
        result = requests.get(self.url)
        content = BeautifulSoup(result.text, 'html.parser')
        links = content.find_all('a', href=re.compile('.mp[4 3]'))
        links = [link.get('href') for link in links] if links else None
        self.music_or_video = 'music' if links[0].endswith('3') else 'video'
        return links

    def get_qualities(self):
        get_links = self.get_all_links()
        available_qualities = []
        if get_links is None:
            raise ExistError('There is no such url :|')
        else:
            for qa in range(len(get_links)):
                if self.music_or_video == 'music':
                    available_qualities.append(music_quality[qa])
                else:
                    available_qualities.append(video_quality[qa])
        return available_qualities

    def get_link(self):
        available_qualities = self.get_qualities()
        links = self.get_all_links()
        if self.quality not in available_qualities:
            raise QualityError(f'this quality does not exist.\nAvailable Quality : {available_qualities}')
        else:
            link = links[available_qualities.index(self.quality)]
            return link


class Main:
    def __init__(self, url, quality):
        self.url = url
        self.quality = quality
        self.scraper = Scraper(self.url, self.quality)

    @property
    def download(self):
        target_url = self.scraper.get_link()
        num_file = 1
        music_or_video = 'video{}.mp4'.format(num_file) \
            if self.scraper.music_or_video == 'video' \
            else 'music.mp3'.format(num_file)
        num_file += 1
        with open(music_or_video, 'wb') as f:
            print('Start Downloading... ')
            result = requests.get(target_url, stream=True)
            total = result.headers.get('content-length')
            if total is None:
                f.write(result.content)
            else:
                download = 0
                total = int(total)
                for data in result.iter_content(chunk_size=4096):
                    f.write(data)
                    download += len(data)
                    done = int(50 * download / total)
                    print('\r[{}{}]'.format('*' * done, ' ' * (50 - done)), end='')
        print('\nFinished Dowloading :)')


a = Main(
    url='https://radiojavanhd.com/112498/%d8%af%d8%a7%d9%86%d9%84%d9%88%d8%af-%d8%a2%d9%87%d9%86%da%af-%d9%85%db%8c%d8%ab%d9%85-%d8%a7%d8%a8%d8%b1%d8%a7%d9%87%db%8c%d9%85%db%8c-%d8%a8%d9%87-%d9%86%d8%a7%d9%85-%d9%85%db%8c%d8%b2%d9%86%d9%87/',
    quality=128)
a.download
