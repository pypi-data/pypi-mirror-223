import hashlib
from functools import partial
import os

import keyring
from textual import on, work
from textual.app import App
from textual.binding import Binding

from lucidwallet.helpers import InitAppResponse, init_app
from lucidwallet.screens import (
    CreateWallet,
    EncryptionPassword,
    FirstRun,
    ImportFromMnemonic,
    MnemonicOverlay,
    WalletLanding,
)

import asyncio

import httpx
import importlib_metadata

package = "lucidwallet"


class FluxWallet(App[None]):
    CSS_PATH = "app.css"
    SCREENS = {
        "welcome": FirstRun(),
        "create_wallet": CreateWallet(),
        "from_mnemonic": ImportFromMnemonic(),
    }
    BINDINGS = [
        ("ctrl+t", "app.toggle_dark", "Toggle Dark mode"),
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit", show=True),
    ]

    async def new_version_available(self) -> str | None:
        current_version = importlib_metadata.version(package)
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://pypi.org/pypi/{package}/json")

        latest_version = response.json()["info"]["version"]

        if current_version != latest_version:
            return latest_version

    @work(name="version_check")
    async def version_check(self) -> None:
        if new_version := await self.new_version_available():
            self.call_after_refresh(
                self.notify, f"New version {new_version} available", timeout=5
            )

    async def valid_password(self, app_data: InitAppResponse) -> bool:
        return await app_data.last_used_wallet.db.validate_key()

    async def encryption_password_callback(
        self, app_data: InitAppResponse, result: tuple[str, bool]
    ) -> None:
        password, store_in_keychain = result

        hashed = hashlib.sha256(bytes(password, "utf8")).hexdigest()
        app_data.last_used_wallet.db.set_encrypted_key(hashed)

        if not await self.valid_password(app_data):
            callback = partial(self.encryption_password_callback, app_data)
            self.push_screen(EncryptionPassword(message="Invalid Password"), callback)
            return

        if store_in_keychain:
            keyring.set_password("fluxwallet", "fluxwallet_user", hashed)

        self.install_screen(
            WalletLanding(
                app_data.last_used_wallet, app_data.networks, app_data.wallets
            ),
            name="wallet_landing",
        )
        self.push_screen("wallet_landing")

    async def on_mount(self) -> None:
        self.version_check()

        # push loading screen first, with logo

        app_data = await init_app()

        if not app_data.last_used_wallet:
            self.push_screen("welcome")
            return

        if app_data.encrypted_db:
            password_hash = keyring.get_password("fluxwallet", "fluxwallet_user")
            # decrypt main key and check for xprv
            if not password_hash:
                callback = partial(self.encryption_password_callback, app_data)
                self.push_screen(EncryptionPassword(), callback)
                return
            else:
                # this only ever needs to get set once
                app_data.last_used_wallet.db.set_encrypted_key(password_hash)

                if not await self.valid_password(app_data):
                    keyring.delete_password("fluxwallet", "fluxwallet_user")

                    callback = partial(self.encryption_password_callback, app_data)
                    self.push_screen(
                        EncryptionPassword(message="Invalid Password"), callback
                    )
                    return

        self.install_screen(
            WalletLanding(
                app_data.last_used_wallet, app_data.networks, app_data.wallets
            ),
            name="wallet_landing",
        )
        self.push_screen("wallet_landing")

    # fix these
    @on(MnemonicOverlay.WalletCreated)
    async def on_mnemonic_overlay_wallet_created(
        self, event: MnemonicOverlay.WalletCreated
    ):
        wallet_landing: WalletLanding = self.get_screen("wallet_landing")
        await wallet_landing.new_wallet_created(event.wallet)

    @on(ImportFromMnemonic.WalletCreated)
    async def on_import_from_mnemonic_wallet_created(
        self, event: ImportFromMnemonic.WalletCreated
    ):
        wallet_landing: WalletLanding = self.get_screen("wallet_landing")
        await wallet_landing.new_wallet_created(event.wallet)


# for console script
def run():
    # ubuntu by default doesn't have this set, so the colors are weird
    os.environ["COLORTERM"] = "truecolor"

    app = FluxWallet()
    app.run()


if __name__ == "__main__":
    run()
