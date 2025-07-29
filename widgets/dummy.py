from widgets.core import Widget, Label


def _callback(label: Label):
    label.text = "Hello"
    return True


labelDummy = Label(
    callback=lambda: _callback(labelDummy)
)

dummmy = Widget(
    content=[labelDummy]
    )
