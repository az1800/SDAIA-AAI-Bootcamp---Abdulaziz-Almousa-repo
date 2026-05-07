import asyncio

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Markdown, Static, LoadingIndicator
from textual.containers import VerticalScroll, Horizontal

from mvc.model import Workflow


class SupportBotApp(App):
    def __init__(self, workflow: Workflow):
        self.workflow = workflow
        super().__init__()

    CSS = """
    Screen { background: #1a1b26; }
    #chat_area { height: 1fr; border: solid #333; padding: 1; margin: 1; }
    Input { dock: bottom; margin: 1; border: double #565f89; }
    .user_msg { color: #7aa2f7; margin-bottom: 1; }
    .bot_msg { color: #9ece6a; margin-bottom: 1; }
    #loading_row { height: auto; align: center middle; margin-top: 1; }
    #loading_row.hidden { display: none; }
    #loading_message { color: #9ece6a; margin-left: 1; }
    """

    BINDINGS = [("q", "quit", "Quit"), ("c", "clear", "Clear Chat")]

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="chat_area"):
            yield Markdown(markdown=self.workflow.messages_to_markdown(), id="history")
            with Horizontal(id="loading_row", classes="hidden"):
                yield LoadingIndicator()
                yield Static("Computing answer...", id="loading_message")
        yield Input(placeholder="Type your message here...")
        yield Footer()

    def on_mount(self) -> None:
        pass

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        user_msg = event.value.strip()
        if not user_msg:
            return
        
        # UI Update: Clear input and show user message, and bot
        event.input.value = ""
        messages = self.workflow.messages_to_markdown()
        buffer = (
            messages +
            "\n\n **👤 User**: " + user_msg +
            "\n\n **🤖 Bot**: "
        )
        widget = self.query_one("#history", Markdown)
        widget.update(buffer)

        # Pass new message to workflow and stream the response into the UI
        async for chunk in self.workflow.astream(message=user_msg):
            buffer += chunk
            widget.update(buffer)
            # sleep to simulate typing
            await asyncio.sleep(0.05)
