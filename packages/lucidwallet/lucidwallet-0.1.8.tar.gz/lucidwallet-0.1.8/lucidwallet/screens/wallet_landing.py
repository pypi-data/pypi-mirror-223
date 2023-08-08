import asyncio
import time
from enum import Enum
from functools import partial

from fluxwallet.db_new import Db, DbAddressBook, DbConfig
from fluxwallet.keys import HDKey
from fluxwallet.values import Value
from fluxwallet.wallet import Wallet, WalletKey, WalletTransaction
from importlib_metadata import version
from rich.console import RenderableType
from sqlalchemy import select
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.message import Message
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Footer, Header, Input, Static, Switch

from lucidwallet.datastore import FluxWalletDataStore, ScanType, Timer
from lucidwallet.events import Event
from lucidwallet.screens import (
    AddressBook,
    ImportKeyToWallet,
    SendTxOverlay,
    SignMessageOverlay,
    TxOverlay,
    TxSentOverlay,
)
from lucidwallet.widgets import Send, TopBar, TransactionHistory

# from textual.css.query import NoMatches


NAV_LINKS = """
[@click="follow_nav('address_book')"]Address Book[/]
[@click="follow_nav('create_wallet')"]Create Wallet[/]
[@click="follow_nav('import_wallet')"]Import Wallet[/]
[@click="follow_nav('import_key')"]Import Key[/]
[@click="follow_nav('encrypt_database')"]Encrypt Database Keys[/]

"""


# class ScanType(Enum):
#     PERIODIC = "PERIODIC"
#     NEW_KEY = "NEW_KEY"
#     FULL_WALLET = "FULL_WALLET"


class FluxWalletError(Exception):
    ...


class Navigation(Static):
    class NavOpened(Message):
        def __init__(self, nav_target: str | None = None) -> None:
            self.nav_target = nav_target
            super().__init__()

    class AddressBookUpdated(Message):
        ...

    def action_follow_nav(self, nav_item: str) -> None:
        self.post_message(self.NavOpened())

        match nav_item:
            case "address_book":
                # do this with post message as currently will reload txs
                self.app.push_screen(AddressBook(), self.on_address_book_update)
            case "import_wallet":
                self.app.push_screen("from_mnemonic")
            case "import_key":
                self.post_message(self.NavOpened(nav_item))
            case "encrypt_database":
                print("WOULD ENCRYPT HERE, NOT BUILT YET")
            case "create_wallet":
                self.app.push_screen("create_wallet")

    def on_address_book_update(self, selected: str | None):
        # shouldn't pass thought the param here from AB.
        self.post_message(self.AddressBookUpdated())


class Version(Static):
    def render(self) -> RenderableType:
        return f"[b]v{version('fluxwallet')}"


class Title(Static):
    pass


class OptionGroup(Container):
    pass


class DarkSwitch(Horizontal):
    def compose(self) -> ComposeResult:
        yield Switch(value=self.app.dark)
        yield Static("Dark mode toggle", classes="label")

    def on_mount(self) -> None:
        self.watch(self.app, "dark", self.on_dark_change, init=False)

    def on_dark_change(self) -> None:
        self.query_one(Switch).value = self.app.dark

    def on_switch_changed(self, event: Switch.Changed) -> None:
        self.app.dark = event.value


class Sidebar(Container):
    def compose(self) -> ComposeResult:
        yield Title("Fluxwallet Menu")
        yield OptionGroup(Navigation(NAV_LINKS), Version())
        yield DarkSwitch()

    def hide(self) -> None:
        self.add_class("-hidden")

    @on(Navigation.NavOpened)
    def on_nav(self):
        self.hide()


class WalletLanding(Screen):
    # CSS_PATH = "wallet.css"
    TITLE = "Fluxwallet"
    BINDINGS = [("ctrl+z", "toggle_sidebar", "Sidebar")]

    show_sidebar = reactive(False)

    class TxSentMessage(Message):
        def __init__(self, txid: str = "", error: bool = None, error_msg: str = ""):
            self.txid = txid
            self.error = error
            self.error_msg = error_msg
            super().__init__()

    class NetworkScanned(Message):
        def __init__(
            self,
            wallet_name: str,
            network_name: str,
            new_transactions: int,
            scan_type: ScanType,
        ) -> None:
            self.wallet_name = wallet_name
            self.network_name = network_name
            self.new_transactions = new_transactions
            self.scan_type = scan_type
            super().__init__()

    def __init__(
        self,
        initial_wallet: Wallet,
        initial_wallet_networks: list[str],
        wallets: list[str],
    ):
        self.initial_wallet = initial_wallet
        self.initial_wallet_networks = initial_wallet_networks

        self.datastore = FluxWalletDataStore(
            wallet_names=set(wallets),
            scan_timer=Timer(self.periodic_scan, 60, run_on_start=True),
        )
        self.tx_events: asyncio.Queue = asyncio.Queue()
        self.update_dom_on_resume = True

        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        # fix this, just pass in defaults and tidy it up after.
        yield TopBar(
            selected_wallet=self.initial_wallet.name,
            selected_network="flux",
            networks=self.initial_wallet_networks,
            wallets=list(self.datastore.wallet_names),
        )
        yield (Horizontal(Send(), TransactionHistory([])))
        yield Footer()

    @work(group="get_tx_from_db_worker")
    async def get_tx_from_db_worker(
        self, force: bool = False, latest_only: bool = False, limit: int = 60
    ) -> None:
        await self.datastore.get_transactions_from_db(
            self.tx_events, force=force, latest_only=latest_only, limit=limit
        )

    async def on_mount(self):
        print("WALLET LANDING ON MOUNT")
        self.monitor_tx_history()

        # just pass in wallet name to WalletLanding, don't open wallet
        await self.datastore.set_current_wallet(self.initial_wallet.name)
        self.datastore.start_scan_timer()
        await self.set_dom_spend_details()
        # self.get_tx_from_db_worker()

        self.initial_wallet = None
        self.initial_wallet_networks = None

        self.db = await Db.start()
        current_address_book = await self.fetch_adress_book()

        send = self.query_one("Send", Send)
        send.update_address_book("", current_address_book)

        self.mount(Sidebar(classes="-hidden"))

    def worker_running(self, worker_name: str) -> bool:
        return bool(next(filter(lambda x: x.group == worker_name, self.workers), None))

    # should this be on the datastore
    async def set_db_last_used_wallet(self, wallet_name: str) -> None:
        async with self.db.get_session() as session:
            await session.merge(
                DbConfig(variable="last_used_wallet", value=wallet_name)
            )
            await session.commit()

    async def fetch_adress_book(self) -> dict[str, str]:
        async with self.db.get_session() as session:
            res = await session.scalars(select(DbAddressBook))
            address_book = res.all()

        return {x.name: x.address for x in address_book}

    def set_dom_wallet_details(self) -> None:
        topbar = self.query_one("TopBar", TopBar)

        current_wallet = self.datastore.current_wallet
        current_network = self.datastore.current_network
        wallets = self.datastore.get_known_wallets()
        networks = self.datastore.get_current_wallet_networks()

        topbar.set_wallet_options(current_wallet, current_network, wallets, networks)

    async def set_dom_spend_details(self) -> None:
        receive_address, balance = await self.datastore.get_current_wallet_spend_info()
        topbar = self.query_one("TopBar", TopBar)
        # temp until I fix api and remove conditional in topbar
        topbar.selected_network = self.datastore.current_network
        topbar.receive_address = receive_address
        topbar.balance = balance

    @work(group="tx_history_updater")
    async def monitor_tx_history(self) -> None:
        tx_history = self.query_one("TransactionHistory", TransactionHistory)

        while True:
            event: Event = await self.tx_events.get()

            match event.type:
                case Event.EventType.NewRows:
                    tx_history.rows = event.rows
                case Event.EventType.ClearTable:
                    tx_history.clear_table()
                case Event.EventType.ScanningStart:
                    await tx_history.set_loading()
                case Event.EventType.ScanningEnd:
                    tx_history.unset_loading()
                case Event.EventType.Scroll:
                    if event.scroll_height:
                        print("scrolling to", event.scroll_height)
                        tx_history.scroll(y=event.scroll_height)

    def tx_history_dom_reload(self) -> None:
        print("TXHISTORY DOM RELOAD")
        self.tx_events.put_nowait(Event(type=Event.EventType.ClearTable))

        self.workers.cancel_group(self, "get_tx_from_db_worker")

        # bit of a hack, keep getting duplicate errors, so only update once finished
        # scanning. Should fix
        if not self.datastore.is_current_network_scanning():
            self.get_tx_from_db_worker()

    async def update_send_address_book(self, selected: str | None = None):
        current_address_book = await self.fetch_adress_book()
        send = self.query_one("Send", Send)
        send.update_address_book(selected, current_address_book)

    def action_toggle_sidebar(self) -> None:
        sidebar = self.query_one("Sidebar", Sidebar)
        # self.set_focus(None)
        if sidebar.has_class("-hidden"):
            sidebar.remove_class("-hidden")
        else:
            if sidebar.query("*:focus"):
                self.screen.set_focus(None)
            sidebar.add_class("-hidden")

    @on(TopBar.WalletSelected)
    async def on_topbar_wallet_selected(self, event: TopBar.WalletSelected) -> None:
        if self.datastore.current_wallet == event.wallet:
            return

        # hack
        send = self.query_one("Send", Send)
        if self.datastore.current_network != "flux":
            send.unmount_disabled()

        await self.set_db_last_used_wallet(event.wallet)
        dt = self.query_one("ScrollCenter", TransactionHistory.ScrollCenter)
        self.datastore.store_current_network_scroll_height(dt.scroll_y)

        await self.datastore.set_current_wallet(event.wallet)

        current_network_scanning = self.datastore.is_current_network_scanning()

        if self.datastore.tx_history_scanning and not current_network_scanning:
            self.datastore.tx_history_scanning = False
            self.tx_events.put_nowait(Event(type=Event.EventType.ScanningEnd))

        if not self.datastore.tx_history_scanning and current_network_scanning:
            self.datastore.tx_history_scanning = True
            self.tx_events.put_nowait(Event(type=Event.EventType.ScanningStart))

        await self.update_dom()
        await self.datastore.reset_timer()

    @on(TopBar.NetworkSelected)
    async def on_topbar_network_selected(self, event: TopBar.NetworkSelected) -> None:
        if self.datastore.current_network == event.network:
            return

        dt = self.query_one("ScrollCenter", TransactionHistory.ScrollCenter)
        self.datastore.store_current_network_scroll_height(dt.scroll_y)

        self.datastore.set_current_network(event.network)

        send = self.query_one("Send", Send)
        if event.network != "flux":
            send.mount_disabled()
        else:
            send.unmount_disabled()

        current_network_scanning = self.datastore.is_current_network_scanning()

        if self.datastore.tx_history_scanning and not current_network_scanning:
            self.tx_events.put_nowait(Event(type=Event.EventType.ScanningEnd))

        if not self.datastore.tx_history_scanning and current_network_scanning:
            self.tx_events.put_nowait(Event(type=Event.EventType.ScanningStart))

        await self.update_dom()
        await self.datastore.reset_timer()

    @on(Send.AddressBookUpdateRequested)
    def on_address_book_update(self, event: Send.AddressBookUpdateRequested) -> None:
        self.app.push_screen(
            AddressBook(event.address, return_nickname=True),
            self.update_send_address_book,
        )
        self.update_dom_on_resume = False

    @on(Navigation.AddressBookUpdated)
    async def on_nav_address_book_updated(self, event: Navigation.AddressBookUpdated):
        await self.update_send_address_book()

    @on(TransactionHistory.TxOverlayRequested)
    async def on_tx_overlay_requested(
        self, event: TransactionHistory.TxOverlayRequested
    ):
        tx = self.datastore.get_transaction(event.txid)
        await tx.sync()
        self.app.push_screen(TxOverlay(tx))
        self.update_dom_on_resume = False

    @on(Send.MaxAmountRequested)
    def set_max_amount(self, event: Send.MaxAmountRequested):
        event.stop()

        amount = self.query_one("#amount", Input)
        balance = self.query_one("TopBar", TopBar).balance
        # fix this - get the fee
        amount.value = str(max(0, float(Value(balance) - Value("225 sat"))))
        amount.focus()

    def tx_overlay_callback(
        self, address: str, amount: float, message: str, send: bool
    ):
        if not send:
            return

        self.send_transaction(address, amount, message)

        self.query_one("Send", Send).clear_fields()

    @on(Send.SendTxRequested)
    def on_send_tx_requested(self, event: Send.SendTxRequested):
        tx_confirm_callback = partial(
            self.tx_overlay_callback, event.address, event.amount, event.message
        )
        self.app.push_screen(
            SendTxOverlay(event.address, event.amount, event.message),
            tx_confirm_callback,
        )
        self.update_dom_on_resume = False

    @on(TxSentMessage)
    async def on_tx_sent(self, event: TxSentMessage):
        self.app.push_screen(TxSentOverlay(event.txid))
        self.update_dom_on_resume = False
        # self.run_worker(self.sync_wallet())
        await self.set_dom_spend_details()

    @on(TopBar.SignMessageRequested)
    async def on_sign_message_requested(self, event: TopBar.SignMessageRequested):
        wallet = self.datastore.get_current_wallet()
        wallet_key = await wallet.get_key(account_id=999, network="bitcoin")
        key = wallet_key.key()
        self.app.push_screen(SignMessageOverlay(key.private_byte))
        self.update_dom_on_resume = False

    @on(ImportKeyToWallet.KeyImportRequested)
    def on_key_import_requested(self, event: ImportKeyToWallet.KeyImportRequested):
        ...

    @on(Navigation.NavOpened)
    def on_nav_opened(self, event: Navigation.NavOpened) -> None:
        match event.nav_target:
            case "import_key":
                self.app.push_screen(
                    ImportKeyToWallet(
                        self.datastore.current_wallet,
                        self.datastore.wallet_names,
                        self.datastore.current_network,
                        self.datastore.get_current_wallet_networks(),
                    ),
                    self.import_key_callback,
                )
                self.update_dom_on_resume = False

    @on(TransactionHistory.ScrollCenter.LazyLoadRequested)
    def on_lazyload_requested(self) -> None:
        if not self.worker_running("get_tx_from_db_worker"):
            self.get_tx_from_db_worker(force=True)

    @on(NetworkScanned)
    async def on_wallet_scanned(self, event: NetworkScanned):
        if (
            event.wallet_name != self.datastore.current_wallet
            and event.network_name != self.datastore.current_network
        ):
            print("current wallet / network not same as scanned network")
            return

        print("NEW TXS", event.new_transactions)

        if event.new_transactions:
            if event.scan_type != ScanType.PERIODIC:
                await self.tx_events.put(Event(type=Event.EventType.ClearTable))

            await self.set_dom_spend_details()

            limit = min(60, event.new_transactions)

            self.get_tx_from_db_worker(force=True, latest_only=True, limit=limit)

    @on(TopBar.RescanAllRequested)
    async def on_rescan_all_requested(self) -> None:
        # self.full_scan_required = True
        self.rescan_wallet()

    async def on_screen_resume(self) -> None:
        # hack until I can think of how to do it better
        if self.update_dom_on_resume:
            await self.update_dom()
        self.update_dom_on_resume = True

    # could probably remove this as a worker
    @work()
    async def import_key_callback(self, result: tuple | None) -> None:
        if not result:
            return

        wallet_name, network_name, private_key = result
        key = HDKey(private_key, network=network_name)

        if (
            wallet_name != self.datastore.current_wallet
            or network_name != self.datastore.current_network
        ):
            await self.datastore.set_current_wallet(wallet_name)
            self.datastore.set_current_network(network_name)
            await self.update_dom()
            await self.datastore.reset_timer()

        wallet = self.datastore.get_current_wallet()

        wallet_key = await wallet.import_key(key, network=network_name)

        if wallet_key:
            self.tx_events.put_nowait(Event(type=Event.EventType.ClearTable))
            self.key_scan(wallet_key)
        else:
            self.app.notify("Key already imported")

    @work()
    async def send_transaction(self, address: str, amount: float, message: str):
        value = Value(amount, network="flux")

        wallet = self.datastore.get_current_wallet()

        wt: WalletTransaction = await wallet.transaction_create(
            [(address, value)], message=message
        )
        # maybe to_thread this. Benchmarked at 5ms. Fine.
        wt.sign()
        await wt.send()

        if wt.pushed:
            message = self.TxSentMessage(wt.tx.txid)
            self.datastore.add_unconfirmed_tx(wt)
            self.get_tx_from_db_worker(force=True, latest_only=True, limit=1)
        else:
            message = self.TxSentMessage(error=True, error_msg=wt.error)

        self.post_message(message)

    async def update_dom(self) -> None:
        await self.set_dom_spend_details()
        self.set_dom_wallet_details()

        # if self.datastore.is_current_network_scanning():
        #     self.tx_events.put_nowait(Event(type=Event.EventType.ScanningStart))

        self.tx_history_dom_reload()

    async def new_wallet_created(self, wallet: Wallet) -> None:
        self.datastore.add_known_wallet(wallet.name)

        await self.datastore.set_current_wallet(wallet)

        self.full_wallet_scan()

    async def update_unconfirmed_txs(self) -> None:
        # fix this whole thing
        for wt in self.datastore.unconfirmed_txs:
            await wt.sync()

            if wt.status == "confirmed":
                date = wt.tx.date.date()
                time = wt.tx.date.strftime("%H:%M:%S")

                tx_history = self.query_one("TransactionHistory", TransactionHistory)
                tx_history.update_date_time(wt.tx.txid, date, time)

        self.datastore.unconfirmed_txs = [
            x for x in self.datastore.unconfirmed_txs if not x.status == "confirmed"
        ]

    def rescan_wallet(self):
        print("SCAN WALLET WORKER")
        # debounce
        if not self.datastore.scan_for_current_network_required(ScanType.FULL_WALLET):
            self.notify("Scanned already")
            return

        self.full_wallet_scan()

    # types of scans
    #
    # periodic, global - shared between all wallets. rerun (reset) on wallet change. Skip if wallet
    # wallet or key scan running for this wallet.
    #
    # new wallet - initial wallet scan
    #
    # new key - initial key scan
    #
    # rescan wallet (same as new wallet scan) if new wallet scan running, skip

    async def periodic_scan(self) -> None:
        print("PERIODIC SCAN")

        if not self.datastore.scan_for_current_network_required(ScanType.PERIODIC):
            print("Scanned within the last 15 sec... returning")
            return

        wallet = self.datastore.get_current_wallet()
        network = self.datastore.get_current_network()

        if self.worker_running("key_scan") or self.worker_running("full_wallet_scan"):
            print("IN PERIODIC SCAN, OTHER SCANS RUNNING.... RETURNING")
            return

        await self.scan_network(wallet, network, scan_type=ScanType.PERIODIC)

    @work(group="key_scan")
    async def key_scan(self, key: WalletKey) -> None:
        self.datastore.reset_current_wallet_datastore()
        wallet = self.datastore.get_current_wallet()
        network = self.datastore.get_current_network()

        await self.scan_network(
            wallet, network=network, key=key, scan_type=ScanType.NEW_KEY
        )

    @work(group="full_wallet_scan")
    async def full_wallet_scan(self) -> None:
        await self.datastore.reset_timer(run_on_start=False)
        self.datastore.reset_current_wallet_datastore()
        self.tx_events.put_nowait(Event(type=Event.EventType.ClearTable))

        wallet = self.datastore.get_current_wallet()
        network = self.datastore.get_current_network()

        await self.scan_network(wallet, network, scan_type=ScanType.FULL_WALLET)

        if self.is_current:
            await self.update_dom()

    def set_scanning_for_network(self, wallet_name: str, network_name: str) -> None:
        self.datastore.set_scanning_for_network(wallet_name, network_name)

        if (
            wallet_name == self.datastore.current_wallet
            and network_name == self.datastore.current_network
            and not self.datastore.tx_history_scanning
        ):
            print("SETTING TX DOM SCANNING")
            self.datastore.tx_history_scanning = True
            self.tx_events.put_nowait(Event(type=Event.EventType.ScanningStart))

    def unset_scanning_for_network(self, wallet_name: str, network_name: str) -> None:
        self.datastore.unset_scanning_for_network(wallet_name, network_name)

        if (
            wallet_name == self.datastore.current_wallet
            and network_name == self.datastore.current_network
            and self.datastore.tx_history_scanning
        ):
            self.datastore.tx_history_scanning = False
            self.tx_events.put_nowait(Event(type=Event.EventType.ScanningEnd))

    async def scan_network(
        self,
        wallet: Wallet,
        network: str,
        scan_type: ScanType,
        *,
        key: WalletKey | None = None,
        # rescan_used: bool = False,
    ) -> None:
        change = 0
        print("SCAN Network", network)

        rescan_used = False

        if not scan_type == ScanType.PERIODIC:
            self.set_scanning_for_network(wallet.name, network)

        if scan_type == ScanType.FULL_WALLET:
            rescan_used = True

        # this is wrong, don't use current
        if self.datastore.is_network_first_scan(wallet.name, network) or rescan_used:
            self.datastore.set_network_scanned(wallet.name, network)
            change = None

        if key:
            new_txids = await wallet.scan_key(key)
        else:
            new_txids = await wallet.scan(
                change=change, rescan_used=rescan_used, network=network
            )

        await self.update_unconfirmed_txs()

        if not scan_type == ScanType.PERIODIC:
            self.unset_scanning_for_network(wallet.name, network)

        if not scan_type == ScanType.NEW_KEY:
            self.datastore.set_last_scanned_for_network(wallet.name, network, scan_type)

        self.post_message(
            self.NetworkScanned(
                wallet.name,
                network,
                scan_type=scan_type,
                new_transactions=len(new_txids),
            )
        )
