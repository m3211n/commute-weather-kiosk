from widgets.core import Widget, Label


class Dummy(Widget):
    def __init__(self):
        super().__init__()

        def _callback():
            return False

        label = Label(
                callback=lambda: _callback(label)
        )

        self.content = [label]
