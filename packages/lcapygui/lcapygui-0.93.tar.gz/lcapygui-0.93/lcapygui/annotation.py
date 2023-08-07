class Annotation:

    def __init__(self, ui, x, y, text):

        self.sketcher = ui.sketcher
        self.x = x
        self.y = y
        self.text = text
        self.patch = None

    @property
    def position(self):

        return self.x, self.y

    def draw(self, **kwargs):

        self.patch = self.sketcher.text(self.x, self.y, self.text, **kwargs)

    def remove(self):

        if self.patch:
            self.patch.remove()
