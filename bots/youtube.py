import os

def download_mp3_from_playlist(playlist_url, output_folder="Youtube Mix Sertanejo"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    command = f'yt-dlp --extract-audio --audio-format mp3 -o "{output_folder}/%(title)s.%(ext)s" {playlist_url}'
    os.system(command)


playlist_url = "https://www.youtube.com/watch?v=kyfXEMqvLgU&list=RDQMbWDpa7a70V8"  # Substitua pela URL da sua playlist
download_mp3_from_playlist(playlist_url)
