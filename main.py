import os

from pytube import YouTube, Playlist

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class YT2MP3(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # image widget
        self.window.add_widget(Image(source='icon.png'))

        # label widget
        self.app_title = Label(text='YouTube to MP3', font_size=20, color='#14edef')
        self.window.add_widget(self.app_title)

        # text input widget
        self.url_input = TextInput(multiline=False, hint_text='Enter YouTube URL', font_size=12, padding_y=(20, 20), size_hint=(1, 0.5))
        self.window.add_widget(self.url_input)

        # button widget
        self.download_button = Button(text='Download', size_hint=(0.5, 0.5), bold=True, background_color='#4e26c6')
        self.download_button.bind(on_press=self.my_callback)
        self.window.add_widget(self.download_button)

        # label widget
        self.status_label = Label(text='Status: ')
        self.window.add_widget(self.status_label)

        return self.window

    def my_callback(self, url_input):
        url = self.url_input.text

        def is_playlist(url):
            if "playlist?list=" in url:
                return "playlist"
            elif "watch?v=" in url:
                return "video"
            else:
                return False
            
        is_playlist = is_playlist(url)

        if is_playlist == "playlist":
            self.status_label.text = 'Status: Downloading playlist...'
            playlist = Playlist(url)
            playlist_name = playlist.title
            if not os.path.exists('playlists'):
                os.makedirs('playlists')
            if not os.path.exists(f'playlists/{playlist_name}'):
                os.makedirs(f'playlists/{playlist_name}')
            for video in playlist.videos:
                self.status_label.text = f'''Status: Downloading playlist...
                {video.title}...'''
                stream = video.streams.filter(only_audio=True).first()
                stream.download(filename=f"playlists/{playlist_name}/{video.title}.mp3")

        elif is_playlist == "video":
            self.status_label.text = 'Status: Downloading video...'
            yt = YouTube(url)
            if not os.path.exists('music'):
                os.makedirs('music')
            stream = yt.streams.filter(only_audio=True).first()
            stream.download(filename=f"music/{yt.title}.mp3")

        else:
            self.status_label.text = "Status: Invalid URL"

if __name__ == '__main__':
    YT2MP3().run()