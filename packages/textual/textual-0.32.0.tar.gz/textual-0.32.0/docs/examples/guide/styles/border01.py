from textual.app import App, ComposeResult
from textual.widgets import Label

TEXT = """I must not fear.
Fear is the mind-killer.
Fear is the little-death that brings total obliteration.
I will face my fear.
I will permit it to pass over me and through me.
And when it has gone past, I will turn the inner eye to see its path.
Where the fear has gone there will be nothing. Only I will remain."""


class BorderApp(App):
    def compose(self) -> ComposeResult:
        self.widget = Label(TEXT)
        yield self.widget

    def on_mount(self) -> None:
        self.widget.styles.background = "darkblue"
        self.widget.styles.width = "50%"
        self.widget.styles.border = ("heavy", "yellow")


if __name__ == "__main__":
    app = BorderApp()
    app.run()
