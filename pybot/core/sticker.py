from pybot.core.thumb import Thumb


class Sticker(object):
    """Represents a Telegram sticker. Accepts sticker json object."""
    def __init__(self, st):
        self.width = st.get('width')
        self.heigth = st.get('height')
        self.thumb = Thumb(st.get('thumb'))
        self.file_id = st.get('file_id')
        self.file_size = st.get('file_size')
