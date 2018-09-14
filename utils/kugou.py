#!/usr/bin/env python
# encoding: utf-8

import os
import json
import requests
import urllib.request


mp3_path = '/home/shengan/audio/mp3'
lyr_path = '/home/shengan/audio/lyric'


def search(keyword):
    url = 'http://songsearch.kugou.com/song_search_v2?keyword={keyword}&page=1&pagesize=1&platform=WebFilter'.format(keyword=keyword)
    r = requests.get(url, verify=False)
    info = json.loads(r.text)
    error_code = info['error_code']
    if error_code != 0:
        raise Exception('url requests error.')
    song = info['data']['lists'][0]
    filename = song['FileName']
    filehash = song['FileHash']
    album_id = song['AlbumID']

    url = 'http://www.kugou.com/yy/index.php?r=play/getdata&hash={filehash}&album_id={album_id}'.format(filehash=filehash, album_id=album_id)
    r = requests.get(url, verify=False)
    info = json.loads(r.text)
    song = info['data']
    play_url = song['play_url']
    lyrics = song['lyrics']
    print(play_url)
    print(lyrics)

    local_name_mp3 = os.path.join(mp3_path, filename + '.mp3')
    urllib.request.urlretrieve(play_url, local_name_mp3)

    local_name_lyr = os.path.join(lyr_path, filename + '.lyr')
    with open(local_name_lyr, 'w') as f:
        # f.write(lyrics.encode('utf8'))
        f.write(lyrics)

    return filename + '.mp3'


if __name__ == '__main__':
    import sys
    key = sys.argv[1]
    # key = r'爱拼才会赢'
    search(key)
