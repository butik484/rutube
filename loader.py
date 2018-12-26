import aiohttp
import youtube_dl
import uvloop
import asyncio
YDL_OPTS = {'format': 'worst[ext=mp4]', 'height': 480}

COMEDY_WOMEN_CHANNEL = 7
SEASON = 8

URL = (
    f'http://rutube.ru/api/metainfo/tv/{COMEDY_WOMEN_CHANNEL}/'
    'video/?season={season}&episode={episode}'
)


async def collect_url(url=None):
    if not url:
        return
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=url,
        ) as resp:
            print(f'Status: {resp.status}')
            response = await resp.json()
            return response['results'][0]


def test(season=None, episode=None):
    return URL.format(season=season, episode=episode)


async def get_video(url):
    """Download video"""
    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
        ydl.download([url])


async def main():
    for i in range(1, 2):
        r = await collect_url(test(season=SEASON, episode=i))
        url = r.get('video_url')
        await get_video(url=url)

#
# if __name__ =='__main__':
#     print('sdads')

loop = uvloop.new_event_loop()
asyncio.set_event_loop(loop)

loop.run_until_complete(main())
