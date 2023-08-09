from dataclasses import dataclass, field

from fluxwallet.db_new import Db, DbConfig, DbWallet
from fluxwallet.wallet import Wallet
from sqlalchemy import select
from textual.widgets import Static

import keyring
from keyring.errors import NoKeyringError
import secrets


class Notification(Static):
    def __init__(self, text: str, variant: str = "success", duration: int = 3):
        super().__init__(text)
        self.duration = duration
        if variant == "success":
            self.styles.outline = ("tall", "green")
        else:
            self.styles.outline = ("tall", "red")

    def on_mount(self) -> None:
        self.set_timer(self.duration, self.remove)

    def on_click(self) -> None:
        self.remove()


@dataclass
class InitAppResponse:
    last_used_wallet: Wallet | None = None
    wallets: list[str] = field(default_factory=list)
    encrypted_db: bool = False
    networks: list[str] = field(default_factory=list)
    keyring_available: bool = False


async def get_db_info() -> tuple[Wallet | None, list[str], bool]:
    db = await Db.start()

    async with db as session:
        last_used_wallet: Wallet | None = None
        res = await session.scalars(select(DbWallet).order_by(DbWallet.id))
        wallets = res.all()

        if wallets:
            res = await session.scalars(
                select(DbConfig.value).filter_by(variable="last_used_wallet")
            )
            last_used_wallet_name = res.first()

            if not last_used_wallet_name:
                last_used_wallet_name = wallets[0].name
                await session.merge(
                    DbConfig(variable="last_used_wallet", value=last_used_wallet_name)
                )
                await session.commit()

            if last_used_wallet_name:
                last_used_wallet = await Wallet.open(last_used_wallet_name)

            wallets = [x.name for x in wallets]
        else:
            wallets = []

    return last_used_wallet, wallets, db.encrypted


async def init_app() -> InitAppResponse:
    last_used_wallet, known_wallets, db_encrypted = await get_db_info()

    random_user = secrets.token_hex(8)

    keyring_available = True
    try:
        # can use empty strings but seems dodgey
        keyring.get_password(random_user, random_user)
    except NoKeyringError:
        keyring_available = False

    wallet_networks = []
    if last_used_wallet:
        # this coudl error
        keys = await last_used_wallet.keys_networks()
        wallet_networks = [x.network.name for x in keys]

    return InitAppResponse(
        last_used_wallet,
        known_wallets,
        db_encrypted,
        wallet_networks,
        keyring_available,
    )
