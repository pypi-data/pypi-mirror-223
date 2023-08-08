from dataclasses import dataclass, field

from fluxwallet.db_new import Db, DbConfig, DbWallet
from fluxwallet.wallet import Wallet
from sqlalchemy import select
from textual.widgets import Static


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


async def get_db_info() -> InitAppResponse:
    db = await Db.start()

    async with db as session:
        last_used_wallet: str | None = None
        res = await session.scalars(select(DbWallet).order_by(DbWallet.id))
        wallets = res.all()

        if wallets:
            res = await session.scalars(
                select(DbConfig.value).filter_by(variable="last_used_wallet")
            )
            last_used_wallet = res.first()

            if not last_used_wallet:
                last_used_wallet = wallets[0].name
                await session.merge(
                    DbConfig(variable="last_used_wallet", value=last_used_wallet)
                )
                await session.commit()

            if last_used_wallet:
                last_used_wallet = await Wallet.open(last_used_wallet)

            wallets = [x.name for x in wallets]
        else:
            wallets = []

    return InitAppResponse(last_used_wallet, wallets, db.encrypted)


async def init_app() -> InitAppResponse:
    res = await get_db_info()

    if res.last_used_wallet:
        # this coudl error
        keys = await res.last_used_wallet.keys_networks()
        res.networks = [x.network.name for x in keys]

    return res
