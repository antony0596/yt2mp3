import os
from pytube import YouTube
from pytube import Playlist

def download_song():
    # download a single video from youtube, audio only
    video_url = input('Paste your video URL here: ')
    yt = YouTube(video_url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download()

    # if music folder doesn't exist, create it
    if not os.path.exists('music'):
        os.makedirs('music')

    # change the file name extension to mp3
    for file in os.listdir():
        if file.endswith('.mp4'):
            os.rename(file, f'{file[:-4]}.mp3')

    # move the file to the music folder, if it exists in destination, replace it
    for file in os.listdir():
        if file.endswith('.mp3'):
            os.replace(file, f'music/{file}')

def download_playlist():
    # download a full playlist from youtube audio only
    print('The playslist must be public (not private or unlisted)')
    playlist_url = input('Type your playlist URL here: ')
    playlist = Playlist(playlist_url)
    for video in playlist.videos:
        stream = video.streams.filter(only_audio=True, file_extension='mp3').first()
        stream.download()

    # if playlists folder doesn't exist, create it
    if not os.path.exists('playlists'):
        os.makedirs('playlists')

    # change the file name extension to mp3
    # for file in os.listdir():
    #     if file.endswith('.mp4'):
    #         name = file
    #         os.rename(file, f'{file[:-4]}.mp3')

    # get the playlist name
    playlist_name = playlist.title

    # if a folder with the playlist name doesn't exist, create it
    if not os.path.exists(f'playlists/{playlist_name}'):
        os.makedirs(f'playlists/{playlist_name}')

    # move the file to the playlist_name folder, if it exists in destination, replace it
    for file in os.listdir():
        if file.endswith('.mp3'):
            os.replace(file, f'playlists/{playlist_name}/{file}')

def main():
    print('''
    1. Download a song
    2. Download a playlist
    ''')
    choice = input('What do you want to do? ')
    if choice == '1':
        download_song()
    elif choice == '2':
        download_playlist()
    else:
        print('Invalid choice.')

main()