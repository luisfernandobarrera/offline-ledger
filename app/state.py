import reflex as rx
from typing import TypedDict, Literal, cast
import datetime
import uuid
import logging
import json
from typing import Any

AccountType = Literal["Asset", "Liability", "Equity", "Revenue", "Expense"]


class Account(TypedDict):
    id: str
    name: str
    code: str
    type: AccountType
    balance: float


class Entry(TypedDict):
    account_id: str
    debit: float
    credit: float


class Transaction(TypedDict):
    id: str
    date: str
    description: str
    entries: list[Entry]


class AppState(rx.State):
    """The main state for the accounting app."""

    active_tab: Literal["accounts", "transactions"] = "accounts"
    accounts_json: str = rx.LocalStorage(
        '[{"id": "'
        + str(uuid.uuid4())
        + '", "name": "Cash", "code": "1010", "type": "Asset", "balance": 10000.0}, {"id": "'
        + str(uuid.uuid4())
        + '", "name": "Accounts Receivable", "code": "1200", "type": "Asset", "balance": 5000.0}, {"id": "'
        + str(uuid.uuid4())
        + '", "name": "Office Supplies", "code": "1510", "type": "Asset", "balance": 500.0}, {"id": "'
        + str(uuid.uuid4())
        + '", "name": "Accounts Payable", "code": "2010", "type": "Liability", "balance": -2000.0}, {"id": "'
        + str(uuid.uuid4())
        + '", "name": "Owner\'s Equity", "code": "3010", "type": "Equity", "balance": -13500.0}, {"id": "'
        + str(uuid.uuid4())
        + '", "name": "Sales Revenue", "code": "4010", "type": "Revenue", "balance": 0.0}, {"id": "'
        + str(uuid.uuid4())
        + '", "name": "Rent Expense", "code": "5010", "type": "Expense", "balance": 0.0}]',
        name="accounts",
    )
    transactions_json: str = rx.LocalStorage("[]", name="transactions")
    accounts: list[Account] = []
    transactions: list[Transaction] = []
    new_account_name: str = ""
    new_account_code: str = ""
    new_account_type: AccountType = "Asset"
    show_account_form: bool = False
    new_transaction_date: str = datetime.date.today().isoformat()
    new_transaction_description: str = ""
    new_transaction_entries: list[dict[str, str | float]] = [
        {"account_id": "", "debit": 0.0, "credit": 0.0},
        {"account_id": "", "debit": 0.0, "credit": 0.0},
    ]
    show_transaction_form: bool = False
    filter_start_date: str = ""
    filter_end_date: str = ""
    filter_description: str = ""
    filter_account_id: str = ""
    filter_min_amount: str = ""
    filter_max_amount: str = ""
    expanded_transaction_id: str = ""
    show_settings: bool = False
    account_types: list[AccountType] = [
        "Asset",
        "Liability",
        "Equity",
        "Revenue",
        "Expense",
    ]

    @rx.event
    def toggle_settings(self):
        self.show_settings = not self.show_settings

    @rx.var
    def account_name_error(self) -> str:
        return "Name cannot be empty." if not self.new_account_name.strip() else ""

    @rx.var
    def account_code_error(self) -> str:
        if not self.new_account_code.strip():
            return "Code cannot be empty."
        if any((acc["code"] == self.new_account_code for acc in self.accounts)):
            return "Code already exists."
        return ""

    @rx.var
    def is_account_form_valid(self) -> bool:
        return not self.account_name_error and (not self.account_code_error)

    @rx.event
    def toggle_account_form(self):
        self.show_account_form = not self.show_account_form
        self._reset_account_form()

    def _reset_account_form(self):
        self.new_account_name = ""
        self.new_account_code = ""
        self.new_account_type = "Asset"

    @rx.event
    def set_active_tab(self, tab_name: Literal["accounts", "transactions"]):
        self.active_tab = tab_name

    @rx.event
    def create_account(self):
        if self.is_account_form_valid:
            new_account: Account = {
                "id": str(uuid.uuid4()),
                "name": self.new_account_name.strip(),
                "code": self.new_account_code.strip(),
                "type": self.new_account_type,
                "balance": 0.0,
            }
            self.accounts.append(new_account)
            self.accounts = sorted(self.accounts, key=lambda acc: acc["code"])
            self.accounts_json = json.dumps(self.accounts)
            self.show_account_form = False
            self._reset_account_form()
            return rx.toast("Account created successfully!", duration=3000)

    @rx.var
    def filtered_transactions(self) -> list[Transaction]:
        """Filters transactions based on the current filter state."""
        transactions_to_filter = self.transactions
        if self.filter_start_date:
            transactions_to_filter = [
                t for t in transactions_to_filter if t["date"] >= self.filter_start_date
            ]
        if self.filter_end_date:
            transactions_to_filter = [
                t for t in transactions_to_filter if t["date"] <= self.filter_end_date
            ]
        if self.filter_description:
            transactions_to_filter = [
                t
                for t in transactions_to_filter
                if self.filter_description.lower() in t["description"].lower()
            ]
        if self.filter_account_id:
            transactions_to_filter = [
                t
                for t in transactions_to_filter
                if any(
                    (e["account_id"] == self.filter_account_id for e in t["entries"])
                )
            ]
        min_amount = float(self.filter_min_amount) if self.filter_min_amount else 0.0
        max_amount = (
            float(self.filter_max_amount) if self.filter_max_amount else float("inf")
        )
        if min_amount > 0 or max_amount < float("inf"):
            transactions_to_filter = [
                t
                for t in transactions_to_filter
                if min_amount <= sum((e["debit"] for e in t["entries"])) <= max_amount
            ]
        return sorted(transactions_to_filter, key=lambda t: t["date"], reverse=True)

    @rx.event
    def set_date_filter_preset(self, preset: str):
        today = datetime.date.today()
        if preset == "today":
            self.filter_start_date = today.isoformat()
            self.filter_end_date = today.isoformat()
        elif preset == "this_week":
            start_of_week = today - datetime.timedelta(days=today.weekday())
            self.filter_start_date = start_of_week.isoformat()
            self.filter_end_date = (
                start_of_week + datetime.timedelta(days=6)
            ).isoformat()
        elif preset == "this_month":
            self.filter_start_date = today.replace(day=1).isoformat()
            self.filter_end_date = today.isoformat()
        elif preset == "this_year":
            self.filter_start_date = today.replace(month=1, day=1).isoformat()
            self.filter_end_date = today.isoformat()
        else:
            self.filter_start_date = ""
            self.filter_end_date = ""

    @rx.event
    def reset_filters(self):
        self.filter_start_date = ""
        self.filter_end_date = ""
        self.filter_description = ""
        self.filter_account_id = ""
        self.filter_min_amount = ""
        self.filter_max_amount = ""

    @rx.event
    def toggle_expand_transaction(self, transaction_id: str):
        if self.expanded_transaction_id == transaction_id:
            self.expanded_transaction_id = ""
        else:
            self.expanded_transaction_id = transaction_id

    @rx.var
    def get_account_map(self) -> dict[str, Account]:
        return {acc["id"]: acc for acc in self.accounts}

    @rx.var
    def total_debits(self) -> float:
        return sum(
            (
                float(entry.get("debit", 0.0) or 0.0)
                for entry in self.new_transaction_entries
            )
        )

    @rx.var
    def total_credits(self) -> float:
        return sum(
            (
                float(entry.get("credit", 0.0) or 0.0)
                for entry in self.new_transaction_entries
            )
        )

    @rx.var
    def transaction_balance(self) -> float:
        return self.total_debits - self.total_credits

    @rx.var
    def is_transaction_balanced(self) -> bool:
        return self.transaction_balance == 0 and self.total_debits > 0

    @rx.var
    def is_transaction_form_valid(self) -> bool:
        if (
            not self.new_transaction_description.strip()
            or not self.is_transaction_balanced
        ):
            return False
        for entry in self.new_transaction_entries:
            if not entry["account_id"]:
                return False
            if (
                float(entry.get("debit", 0.0) or 0.0) < 0
                or float(entry.get("credit", 0.0) or 0.0) < 0
            ):
                return False
            if (
                float(entry.get("debit", 0.0) or 0.0) > 0
                and float(entry.get("credit", 0.0) or 0.0) > 0
            ):
                return False
        return True

    @rx.event
    def toggle_transaction_form(self):
        self.show_transaction_form = not self.show_transaction_form
        self._reset_transaction_form()

    def _reset_transaction_form(self):
        self.new_transaction_date = datetime.date.today().isoformat()
        self.new_transaction_description = ""
        self.new_transaction_entries = [
            {"account_id": "", "debit": 0.0, "credit": 0.0},
            {"account_id": "", "debit": 0.0, "credit": 0.0},
        ]

    @rx.event
    def add_entry_row(self):
        self.new_transaction_entries.append(
            {"account_id": "", "debit": 0.0, "credit": 0.0}
        )

    @rx.event
    def remove_entry_row(self, index: int):
        if len(self.new_transaction_entries) > 2:
            self.new_transaction_entries.pop(index)

    @rx.event
    def update_entry(self, index: int, field: str, value: str):
        entry = self.new_transaction_entries[index]
        if field in ["debit", "credit"]:
            try:
                entry[field] = float(value)
            except (ValueError, TypeError) as e:
                logging.exception(f"Error converting value to float: {e}")
                entry[field] = 0.0
            if field == "debit" and entry[field] > 0:
                entry["credit"] = 0.0
            elif field == "credit" and entry[field] > 0:
                entry["debit"] = 0.0
        else:
            entry[field] = value

    @rx.event
    def create_transaction(self):
        if self.is_transaction_form_valid:
            valid_entries = [
                e
                for e in self.new_transaction_entries
                if float(e.get("debit", 0) or 0) > 0
                or float(e.get("credit", 0) or 0) > 0
            ]
            new_transaction: Transaction = {
                "id": str(uuid.uuid4()),
                "date": self.new_transaction_date,
                "description": self.new_transaction_description.strip(),
                "entries": [
                    {
                        "account_id": cast(str, entry["account_id"]),
                        "debit": float(entry.get("debit", 0.0) or 0.0),
                        "credit": float(entry.get("credit", 0.0) or 0.0),
                    }
                    for entry in valid_entries
                ],
            }
            self.transactions.append(new_transaction)
            self.transactions_json = json.dumps(self.transactions)
            for entry in new_transaction["entries"]:
                for i, acc in enumerate(self.accounts):
                    if acc["id"] == entry["account_id"]:
                        if acc["type"] in ["Asset", "Expense"]:
                            self.accounts[i]["balance"] += (
                                entry["debit"] - entry["credit"]
                            )
                        else:
                            self.accounts[i]["balance"] += (
                                entry["credit"] - entry["debit"]
                            )
                        break
            self.accounts_json = json.dumps(self.accounts)
            self.show_transaction_form = False
            self._reset_transaction_form()
            return rx.toast("Transaction created successfully!", duration=3000)

    @rx.event
    def load_from_storage(self):
        try:
            self.accounts = json.loads(self.accounts_json)
        except json.JSONDecodeError as e:
            logging.exception(f"Error decoding accounts_json: {e}")
            self.accounts = []
        try:
            self.transactions = json.loads(self.transactions_json)
        except json.JSONDecodeError as e:
            logging.exception(f"Error decoding transactions_json: {e}")
            self.transactions = []
        self.accounts = sorted(self.accounts, key=lambda acc: acc["code"])

    @rx.event
    def export_data(self) -> rx.event.EventSpec:
        data_to_export = {"accounts": self.accounts, "transactions": self.transactions}
        return rx.download(
            data=json.dumps(data_to_export, indent=2),
            filename=f"accounting_backup_{datetime.date.today().isoformat()}.json",
        )

    @rx.event
    async def import_data(self, files: list[rx.UploadFile]):
        if not files:
            return rx.toast("No file selected.", duration=3000)
        try:
            file_content = await files[0].read()
            data = json.loads(file_content)
            if "accounts" in data and "transactions" in data:
                self.accounts = data["accounts"]
                self.transactions = data["transactions"]
                self.accounts_json = json.dumps(self.accounts)
                self.transactions_json = json.dumps(self.transactions)
                self.accounts = sorted(self.accounts, key=lambda acc: acc["code"])
                self.show_settings = False
                return rx.toast("Data imported successfully!", duration=3000)
            return rx.toast("Invalid backup file format.", duration=3000)
        except Exception as e:
            logging.exception(f"Error importing data: {e}")
            return rx.toast(f"Error importing data: {e}", duration=5000)

    @rx.event
    def clear_all_data(self):
        self.accounts = []
        self.transactions = []
        self.accounts_json = "[]"
        self.transactions_json = "[]"
        self.show_settings = False
        return rx.toast("All data has been cleared.", duration=3000)