from functools import partial

from fluxwallet.mnemonic import Mnemonic
from textual.app import ComposeResult
from textual.containers import Grid, Horizontal
from textual.message import Message
from textual.reactive import var
from textual.screen import Screen
from textual.validation import Length
from textual.widget import Widget
from textual.widgets import Button, Input, Label, Select, Static

from lucidwallet.helpers import init_app
from lucidwallet.screens import MnemonicOverlay

languages = [
    "english",
    "spanish",
    "italian",
    "dutch",
    "french",
    "japanese",
    "chinese_simplified",
    "chinese_traditional",
]


# class Notification(Static):
#     def on_mount(self) -> None:
#         self.set_timer(3, self.remove)

#     def on_click(self) -> None:
#         self.remove()


class LanguagePicker(Widget):
    def __init__(self, language: str = "english"):
        self.language = language
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label("Select Language")
        yield Select(
            [(x, x) for x in languages],
            prompt="Select language",
            value=self.language,
        )

    def reset(self) -> None:
        self.language = "english"
        select = self.query_one("Select", Select)
        select.value = "english"

    def on_select_changed(self, event: Select.Changed):
        self.language = event.value


class CreateWallet(Screen):
    BINDINGS = [
        (
            "escape",
            "app.pop_screen()",
            "home",
        ),
    ]

    nickname = var("")

    # class WalletLandingRequested(Message):
    #     def __init__(self, wallet: str, wallets: list[str], networks: list[str]):
    #         self.wallet = wallet
    #         self.wallets = wallets
    #         self.networks = networks
    #         super().__init__()

    def compose(self):
        yield Static("Create Wallet", id="create_wallet_title")
        yield LanguagePicker()
        yield Input(
            "",
            placeholder="Wallet nickname",
            id="nickname",
            validators=[Length(maximum=15, minimum=2)],
        )
        yield Grid(id="mnemonic_grid")
        yield Horizontal(
            Button("Cancel", variant="warning", id="wallet_create_cancel"),
            Button("Create", id="wallet_create", disabled=True),
            id="create_wallet_button_container",
        )

    def on_mount(self) -> None:
        input = self.query_one("Input", Input)
        input.focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.validation_result.failures:
            # self.mount(
            #     Notification(event.validation_result.failures, variant="failure")
            # )
            return

        if event.value:
            self.nickname = event.value

    def reset_all(self) -> None:
        self.nickname = ""
        input = self.query_one("Input", Input)
        input.value = ""
        lang_picker = self.query_one("LanguagePicker", LanguagePicker)
        lang_picker.reset()
        input.focus()

    async def on_button_pressed(self, event: Button.Pressed):
        event.stop()
        if event.button.id == "wallet_create":
            print("WALLET CREATE")
            # wallet_name = self.query_one("Input", Input)
            app_data = await init_app()
            if self.nickname in app_data.wallets:
                self.notify("Wallet name exists")
                return

            lang_picker = self.query_one("LanguagePicker", LanguagePicker)
            mnemonic = Mnemonic(lang_picker.language).generate()

            self.app.push_screen(MnemonicOverlay(self.nickname, mnemonic))

            self.reset_all()
        else:
            self.reset_all()
            self.dismiss()

    def watch_nickname(self, new_value) -> None:
        create = self.query_one("#wallet_create", Button)

        if new_value:
            create.disabled = False
        else:
            create.disabled = True
