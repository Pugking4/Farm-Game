class Message():
    def __init__(self, text: str, frames: int, fade: bool=True):
        self.text = text
        self.frames = frames
        self.fade_in = (frames*fade, int(frames - frames/20)*fade)
        self.fade_out = (int(int(frames/20))*fade, 0*fade)
        self.fade = frames/20
        if fade:
            self.alpha = 0
        else:
            self.alpha = 255
