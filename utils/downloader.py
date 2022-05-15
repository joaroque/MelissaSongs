import youtube_dl


def downloader(dest, file_name: str, link: str) -> None:
    path = dest + file_name + '.mp3'
    ydl_opts = {
        'outtmpl': path,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '256',
        }],
        'prefer_ffmpeg': True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=True)

    return path