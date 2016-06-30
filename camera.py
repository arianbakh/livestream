import os
import time
from StringIO import StringIO

from PIL import Image, ImageFont, ImageDraw

from configuration import FONTS_DIR


RESOLUTIONS = {
    '4k': (3840, 2160),
    '1080p': (1920, 1080),
    '720p': (1280, 720),
    '480p': (640, 480),
    '360p': (480, 360),
    '240p': (426, 240),
    '144p': (256, 144),
}


class Camera(object):
    frames_count = 60
    resolution = RESOLUTIONS['720p']
    background_color = (50, 50, 100)
    text_color = (225, 255, 255)

    def __init__(self):
        font_path = os.path.join(FONTS_DIR, 'Roboto-Regular.ttf')
        font_size = self.resolution[0] / 10
        self.font = ImageFont.truetype(font_path, font_size)

        self.current_frame_index = 0

        self.last_frame_lsd = -1  # least significant digit
        self.last_second_frames = 0

        self.background_image = Image.new('RGB', self.resolution, self.background_color)

        self.frame = self._get_frame_by_frame_rate(0)

    def _get_frame_by_frame_rate(self, frame_rate):
        tmp_image = self.background_image.copy()
        draw = ImageDraw.Draw(tmp_image)
        draw.text((0, 0), 'FPS: %d' % frame_rate, font=self.font, fill=self.text_color)
        image_file = StringIO()
        tmp_image.save(image_file, 'jpeg')
        return image_file.getvalue()

    def get_frame(self):
        current_time_lsd = int(time.time()) % 10
        if current_time_lsd == self.last_frame_lsd:
            self.last_second_frames += 1
        else:
            self.last_frame_lsd = current_time_lsd
            self.frame = self._get_frame_by_frame_rate(self.last_second_frames)
            self.last_second_frames = 0

        return self.frame
