
import requests
import re


class PlayHT:
    def __init__(self, user_id, secret_key):
        self.user_id = user_id
        self.secret_key = secret_key
        self.headers = {
            'AUTHORIZATION': f'Bearer {self.secret_key}',
            'X-USER-ID': self.user_id,
            'accept': 'text/event-stream',
            'content-type': 'application/json'
        }

    def get_mp3_url(self, text, voice):
        response = requests.post("https://play.ht/api/v2/tts",
                                 headers=self.headers,
                                 json={
                                        "text": text,
                                        "voice": voice
                                 },
                                 stream=True)
        chunk_list = []
        if response.status_code == 200:
            for chunk in response.iter_content(chunk_size=3):
                if chunk:
                    chunk_list.append(chunk.decode('utf-8'))

        chunk_data = ''.join(chunk_list)
        url = re.findall(r'"url":"(.*?)"', chunk_data)
        if len(url) > 0:
            return url[0]
        else:
            return None

    def download_mp3(self, url, filename):
        doc = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(doc.content)

    def tts(self, text, voice, filename):
        url = self.get_mp3_url(text=text, voice=voice)
        if url is not None:
            self.download_mp3(url=url, filename=filename)
        else:
            print("Error: url is None")
