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

    active_tab: Literal["accounts", "transactions", "reports", "dashboard"] = "accounts"
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
    language: str = rx.LocalStorage("en", name="language")
    available_languages: list[dict[str, str]] = [
        {"code": "en", "name": "English", "flag": "🇬🇧"},
        {"code": "es", "name": "Español", "flag": "🇪🇸"},
        {"code": "fr", "name": "Français", "flag": "🇫🇷"},
        {"code": "zh", "name": "中文", "flag": "🇨🇳"},
        {"code": "pt", "name": "Português", "flag": "🇵🇹"},
    ]
    # Report-related state
    active_report_tab: Literal["trial_balance", "balance_sheet", "income_statement", "general_ledger"] = "trial_balance"
    report_date: str = datetime.date.today().isoformat()
    report_start_date: str = datetime.date.today().replace(day=1).isoformat()
    report_end_date: str = datetime.date.today().isoformat()
    general_ledger_account_id: str = ""
    # UI state
    # Persisted as string to avoid type-mismatch with LocalStorage
    dark_mode_str: str = rx.LocalStorage("false", name="dark_mode")

    @rx.var
    def is_dark_mode(self) -> bool:
        return str(self.dark_mode_str).lower() == "true"

    @rx.var
    def t(self) -> dict[str, str]:
        from app.i18n import translations

        return translations.get(self.language, translations["en"])

    @rx.event
    def set_language(self, lang_code: str):
        self.language = lang_code

    @rx.event
    def toggle_settings(self):
        self.show_settings = not self.show_settings
    
    @rx.event
    def toggle_dark_mode(self):
        # Flip the stored string value
        current = str(self.dark_mode_str).lower() == "true"
        self.dark_mode_str = "true" if not current else "false"
    
    # Explicit setters for filter fields (to avoid deprecation warnings)
    @rx.event
    def set_filter_start_date(self, value: str):
        self.filter_start_date = value
    
    @rx.event
    def set_filter_end_date(self, value: str):
        self.filter_end_date = value
    
    @rx.event
    def set_filter_description(self, value: str):
        self.filter_description = value
    
    @rx.event
    def set_filter_account_id(self, value: str):
        self.filter_account_id = value
    
    @rx.event
    def set_filter_min_amount(self, value: float):
        # Store as string for consistent filtering and UI binding
        try:
            if value is None:
                self.filter_min_amount = ""
            else:
                # Allow both float and str inputs
                numeric = float(value)
                # Treat 0.0 same as unset to preserve semantics
                self.filter_min_amount = "" if numeric == 0.0 else str(numeric)
        except (ValueError, TypeError):
            self.filter_min_amount = ""
    
    @rx.event
    def set_filter_max_amount(self, value: float):
        # Store as string for consistent filtering and UI binding
        try:
            if value is None:
                self.filter_max_amount = ""
            else:
                numeric = float(value)
                self.filter_max_amount = "" if numeric == 0.0 else str(numeric)
        except (ValueError, TypeError):
            self.filter_max_amount = ""
    
    # Explicit setters for report fields
    @rx.event
    def set_report_date(self, value: str):
        self.report_date = value
    
    @rx.event
    def set_report_start_date(self, value: str):
        self.report_start_date = value
    
    @rx.event
    def set_report_end_date(self, value: str):
        self.report_end_date = value
    
    # Explicit setters for account form fields
    @rx.event
    def set_new_account_name(self, value: str):
        self.new_account_name = value
    
    @rx.event
    def set_new_account_code(self, value: str):
        self.new_account_code = value
    
    @rx.event
    def set_new_account_type(self, value: AccountType):
        self.new_account_type = value
    
    # Explicit setters for transaction form fields
    @rx.event
    def set_new_transaction_date(self, value: str):
        self.new_transaction_date = value
    
    @rx.event
    def set_new_transaction_description(self, value: str):
        self.new_transaction_description = value

    @rx.var
    def account_name_error(self) -> str:
        return self.t["error_name_empty"] if not self.new_account_name.strip() else ""

    @rx.var
    def account_code_error(self) -> str:
        if not self.new_account_code.strip():
            return self.t["error_code_empty"]
        if any((acc["code"] == self.new_account_code for acc in self.accounts)):
            return self.t["error_code_exists"]
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
    def set_active_tab(self, tab_name: Literal["accounts", "transactions", "reports", "dashboard"]):
        self.active_tab = tab_name
    
    @rx.event
    def set_active_report_tab(self, tab_name: Literal["trial_balance", "balance_sheet", "income_statement", "general_ledger"]):
        self.active_report_tab = tab_name
    
    @rx.event
    def set_general_ledger_account_id(self, account_id: str):
        self.general_ledger_account_id = account_id

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
            return rx.toast(self.t["toast_account_created"], duration=3000)

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

    @rx.var
    def filtered_transaction_count(self) -> int:
        return len(self.filtered_transactions)

    @rx.var
    def total_transaction_count(self) -> int:
        return len(self.transactions)

    @rx.var
    def filtered_count_badge(self) -> str:
        return f"{self.filtered_transaction_count}/{self.total_transaction_count}"

    @rx.var
    def filtered_transactions_rows(self) -> list[dict]:
        rows: list[dict] = []
        for t in self.filtered_transactions:
            total = sum(float(e.get("debit", 0.0) or 0.0) for e in t.get("entries", []))
            rows.append({
                "id": t["id"],
                "date": t["date"],
                "description": t["description"],
                "entries": t["entries"],
                "total": round(total, 2),
            })
        return rows

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
    def entries_for_expanded(self) -> list[Entry]:
        if not self.expanded_transaction_id:
            return []
        txn = next((t for t in self.transactions if t["id"] == self.expanded_transaction_id), None)
        if not txn:
            return []
        # Ensure types are normalized
        fixed: list[Entry] = []
        for e in txn.get("entries", []):
            try:
                debit = float(e.get("debit", 0.0) or 0.0)
            except Exception:
                debit = 0.0
            try:
                credit = float(e.get("credit", 0.0) or 0.0)
            except Exception:
                credit = 0.0
            fixed.append({
                "account_id": str(e.get("account_id", "")),
                "debit": debit,
                "credit": credit,
            })
        return fixed

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
            return rx.toast(self.t["toast_transaction_created"], duration=3000)

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
        # Default preset to All Time on first load if there are transactions and no date filter
        if self.transactions and not (self.filter_start_date or self.filter_end_date):
            self.set_date_filter_preset("all")

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
            return rx.toast(self.t["toast_no_file"], duration=3000)
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
                return rx.toast(self.t["toast_import_success"], duration=3000)
            return rx.toast(self.t["toast_invalid_backup"], duration=3000)
        except Exception as e:
            logging.exception(f"Error importing data: {e}")
            return rx.toast(f"{self.t['toast_import_error']}: {e}", duration=5000)

    @rx.event
    def clear_all_data(self):
        self.accounts = []
        self.transactions = []
        self.accounts_json = "[]"
        self.transactions_json = "[]"
        self.show_settings = False
        return rx.toast(self.t["toast_data_cleared"], duration=3000)
    
    @rx.event
    def normalize_data(self):
        """Coerce legacy transaction shapes to the expected schema and persist."""
        try:
            # Ensure in-memory data is up to date with storage
            try:
                self.accounts = json.loads(self.accounts_json)
            except Exception:
                pass
            try:
                self.transactions = json.loads(self.transactions_json)
            except Exception:
                pass

            normalized: list[Transaction] = []
            for txn in self.transactions or []:
                # Basic fields
                txn_id = str(txn.get("id") or uuid.uuid4())
                # Coerce date to ISO yyyy-mm-dd if possible
                raw_date = txn.get("date") or txn.get("created_at") or datetime.date.today().isoformat()
                try:
                    # Accept already-ISO or parseable dates
                    date_iso = str(raw_date)
                    if len(date_iso) >= 10 and date_iso[4] == '-' and date_iso[7] == '-':
                        pass
                    else:
                        date_iso = datetime.date.fromisoformat(str(raw_date)).isoformat()
                except Exception:
                    date_iso = datetime.date.today().isoformat()
                description = str(txn.get("description") or txn.get("memo") or "")

                entries = txn.get("entries") or txn.get("lines") or []
                fixed_entries: list[Entry] = []
                for e in entries:
                    account_id = str(e.get("account_id") or e.get("account") or "")
                    # Coerce debit/credit to non-negative floats
                    def to_amount(x: Any) -> float:
                        try:
                            if x in (None, ""):
                                return 0.0
                            return float(x)
                        except Exception:
                            return 0.0

                    debit = abs(to_amount(e.get("debit")))
                    credit = abs(to_amount(e.get("credit")))
                    # If both present, keep the larger and zero the other
                    if debit > 0 and credit > 0:
                        if debit >= credit:
                            credit = 0.0
                        else:
                            debit = 0.0
                    fixed_entries.append({
                        "account_id": account_id,
                        "debit": debit,
                        "credit": credit,
                    })

                normalized.append({
                    "id": txn_id,
                    "date": date_iso,
                    "description": description,
                    "entries": fixed_entries,
                })

            self.transactions = normalized
            self.transactions_json = json.dumps(self.transactions)
            # Keep accounts list persisted and sorted
            try:
                self.accounts = sorted(self.accounts, key=lambda acc: acc["code"]) if self.accounts else []
                self.accounts_json = json.dumps(self.accounts)
            except Exception:
                pass
            return rx.toast("Data normalized.", duration=3000)
        except Exception as e:
            logging.exception(f"Error normalizing data: {e}")
            return rx.toast(f"Normalize failed: {e}", duration=5000)
    
    @rx.event
    def recompute_balances_from_transactions(self):
        """Re-derive all account balances strictly from transactions."""
        try:
            # Ensure in-memory mirrors persisted data
            try:
                self.accounts = json.loads(self.accounts_json)
            except Exception:
                pass
            try:
                self.transactions = json.loads(self.transactions_json)
            except Exception:
                pass

            # Initialize per-account balances
            account_type_by_id: dict[str, str] = {acc["id"]: acc["type"] for acc in self.accounts}
            new_balance_by_id: dict[str, float] = {acc_id: 0.0 for acc_id in account_type_by_id.keys()}

            # Accumulate from every transaction entry
            for txn in self.transactions or []:
                for e in txn.get("entries", []):
                    acc_id = str(e.get("account_id") or "")
                    if not acc_id or acc_id not in new_balance_by_id:
                        # Skip entries that reference unknown accounts
                        continue
                    try:
                        debit = float(e.get("debit", 0.0) or 0.0)
                    except Exception:
                        debit = 0.0
                    try:
                        credit = float(e.get("credit", 0.0) or 0.0)
                    except Exception:
                        credit = 0.0
                    acc_type = account_type_by_id.get(acc_id, "Asset")
                    if acc_type in ["Asset", "Expense"]:
                        delta = debit - credit
                    else:
                        delta = credit - debit
                    new_balance_by_id[acc_id] += delta

            # Write back rounded balances
            updated_accounts: list[Account] = []
            for acc in self.accounts:
                updated = dict(acc)
                updated["balance"] = round(new_balance_by_id.get(acc["id"], 0.0), 2)
                updated_accounts.append(updated)
            self.accounts = updated_accounts
            self.accounts_json = json.dumps(self.accounts)
            return rx.toast("Balances recomputed from transactions.", duration=3000)
        except Exception as e:
            logging.exception(f"Error recomputing balances: {e}")
            return rx.toast(f"Recompute failed: {e}", duration=5000)
        
    # Report computed properties
    @rx.var
    def trial_balance_data(self) -> list[dict]:
        """Returns trial balance data with debit/credit columns."""
        result = []
        for acc in self.accounts:
            balance = acc["balance"]
            debit = balance if balance > 0 else 0.0
            credit = abs(balance) if balance < 0 else 0.0
            result.append({
                "code": acc["code"],
                "name": acc["name"],
                "type": acc["type"],
                "debit": debit,
                "credit": credit,
            })
        return result
    
    @rx.var
    def trial_balance_total_debits(self) -> float:
        return sum(item["debit"] for item in self.trial_balance_data)
    
    @rx.var
    def trial_balance_total_credits(self) -> float:
        return sum(item["credit"] for item in self.trial_balance_data)
    
    @rx.var
    def balance_sheet_assets(self) -> list[Account]:
        return [acc for acc in self.accounts if acc["type"] == "Asset"]
    
    @rx.var
    def balance_sheet_liabilities(self) -> list[Account]:
        return [acc for acc in self.accounts if acc["type"] == "Liability"]
    
    @rx.var
    def balance_sheet_equity(self) -> list[Account]:
        return [acc for acc in self.accounts if acc["type"] == "Equity"]
    
    @rx.var
    def total_assets(self) -> float:
        return sum(acc["balance"] for acc in self.balance_sheet_assets)
    
    @rx.var
    def total_liabilities(self) -> float:
        return abs(sum(acc["balance"] for acc in self.balance_sheet_liabilities))
    
    @rx.var
    def total_equity(self) -> float:
        return abs(sum(acc["balance"] for acc in self.balance_sheet_equity))
    
    @rx.var
    def total_liabilities_equity(self) -> float:
        return self.total_liabilities + self.total_equity
    
    @rx.var
    def income_statement_revenue(self) -> list[Account]:
        return [acc for acc in self.accounts if acc["type"] == "Revenue"]
    
    @rx.var
    def income_statement_expenses(self) -> list[Account]:
        return [acc for acc in self.accounts if acc["type"] == "Expense"]
    
    @rx.var
    def total_revenue(self) -> float:
        return abs(sum(acc["balance"] for acc in self.income_statement_revenue))
    
    @rx.var
    def total_expenses(self) -> float:
        return sum(acc["balance"] for acc in self.income_statement_expenses)
    
    @rx.var
    def net_income(self) -> float:
        return self.total_revenue - self.total_expenses
    
    @rx.var
    def general_ledger_entries(self) -> list[dict]:
        """Returns entries for the selected account with running balance."""
        if not self.general_ledger_account_id:
            return []
        
        entries = []
        running_balance = 0.0
        
        # Get account type to determine balance calculation
        account = next((acc for acc in self.accounts if acc["id"] == self.general_ledger_account_id), None)
        if not account:
            return []
        
        account_type = account["type"]
        
        # Collect all entries for this account
        for txn in sorted(self.transactions, key=lambda t: t["date"]):
            for entry in txn["entries"]:
                if entry["account_id"] == self.general_ledger_account_id:
                    # Calculate running balance based on account type
                    if account_type in ["Asset", "Expense"]:
                        running_balance += entry["debit"] - entry["credit"]
                    else:
                        running_balance += entry["credit"] - entry["debit"]
                    
                    entries.append({
                        "date": txn["date"],
                        "description": txn["description"],
                        "debit": entry["debit"],
                        "credit": entry["credit"],
                        "running_balance": running_balance,
                    })
        
        return entries
    
    @rx.event
    def export_report_csv(self) -> rx.event.EventSpec:
        """Export current report as CSV."""
        import csv
        import io
        
        output = io.StringIO()
        
        if self.active_report_tab == "trial_balance":
            writer = csv.writer(output)
            writer.writerow(["Code", "Account Name", "Debit", "Credit"])
            for item in self.trial_balance_data:
                writer.writerow([
                    item["code"],
                    item["name"],
                    f"{item['debit']:.2f}" if item["debit"] > 0 else "",
                    f"{item['credit']:.2f}" if item["credit"] > 0 else "",
                ])
            writer.writerow(["", "Total", f"{self.trial_balance_total_debits:.2f}", f"{self.trial_balance_total_credits:.2f}"])
            filename = f"trial_balance_{self.report_date}.csv"
        
        elif self.active_report_tab == "balance_sheet":
            writer = csv.writer(output)
            writer.writerow(["Balance Sheet", f"As of {self.report_date}"])
            writer.writerow([])
            writer.writerow(["ASSETS"])
            for acc in self.balance_sheet_assets:
                writer.writerow([f"{acc['code']} - {acc['name']}", f"{acc['balance']:.2f}"])
            writer.writerow(["Total Assets", f"{self.total_assets:.2f}"])
            writer.writerow([])
            writer.writerow(["LIABILITIES"])
            for acc in self.balance_sheet_liabilities:
                writer.writerow([f"{acc['code']} - {acc['name']}", f"{abs(acc['balance']):.2f}"])
            writer.writerow(["Total Liabilities", f"{self.total_liabilities:.2f}"])
            writer.writerow([])
            writer.writerow(["EQUITY"])
            for acc in self.balance_sheet_equity:
                writer.writerow([f"{acc['code']} - {acc['name']}", f"{abs(acc['balance']):.2f}"])
            writer.writerow(["Total Equity", f"{self.total_equity:.2f}"])
            writer.writerow([])
            writer.writerow(["Total Liabilities & Equity", f"{self.total_liabilities_equity:.2f}"])
            filename = f"balance_sheet_{self.report_date}.csv"
        
        elif self.active_report_tab == "income_statement":
            writer = csv.writer(output)
            writer.writerow(["Income Statement", f"{self.report_start_date} to {self.report_end_date}"])
            writer.writerow([])
            writer.writerow(["REVENUE"])
            for acc in self.income_statement_revenue:
                writer.writerow([f"{acc['code']} - {acc['name']}", f"{abs(acc['balance']):.2f}"])
            writer.writerow(["Total Revenue", f"{self.total_revenue:.2f}"])
            writer.writerow([])
            writer.writerow(["EXPENSES"])
            for acc in self.income_statement_expenses:
                writer.writerow([f"{acc['code']} - {acc['name']}", f"{acc['balance']:.2f}"])
            writer.writerow(["Total Expenses", f"{self.total_expenses:.2f}"])
            writer.writerow([])
            writer.writerow(["Net Income", f"{self.net_income:.2f}"])
            filename = f"income_statement_{self.report_start_date}_{self.report_end_date}.csv"
        
        else:  # general_ledger
            writer = csv.writer(output)
            writer.writerow(["Date", "Description", "Debit", "Credit", "Balance"])
            for entry in self.general_ledger_entries:
                writer.writerow([
                    entry["date"],
                    entry["description"],
                    f"{entry['debit']:.2f}" if entry["debit"] > 0 else "",
                    f"{entry['credit']:.2f}" if entry["credit"] > 0 else "",
                    f"{entry['running_balance']:.2f}",
                ])
            filename = f"general_ledger_{self.general_ledger_account_id}_{datetime.date.today().isoformat()}.csv"
        
        csv_data = output.getvalue()
        return rx.download(data=csv_data, filename=filename)
    
    # Dashboard computed properties
    @rx.var
    def recent_transactions(self) -> list[Transaction]:
        """Returns the 10 most recent transactions."""
        return sorted(self.transactions, key=lambda t: t["date"], reverse=True)[:10]
    
    @rx.var
    def asset_count(self) -> int:
        return len([acc for acc in self.accounts if acc["type"] == "Asset"])
    
    @rx.var
    def liability_count(self) -> int:
        return len([acc for acc in self.accounts if acc["type"] == "Liability"])
    
    @rx.var
    def equity_count(self) -> int:
        return len([acc for acc in self.accounts if acc["type"] == "Equity"])
    
    @rx.var
    def revenue_count(self) -> int:
        return len([acc for acc in self.accounts if acc["type"] == "Revenue"])
    
    @rx.var
    def expense_count(self) -> int:
        return len([acc for acc in self.accounts if acc["type"] == "Expense"])