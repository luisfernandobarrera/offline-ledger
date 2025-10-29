import reflex as rx
from app.state import AppState
from app.components import form_field
from datetime import datetime


def reports_view() -> rx.Component:
    """Main reports view with tabs for different report types."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                AppState.t["reports"],
                class_name="text-xl font-semibold text-gray-700 mb-6 font-['JetBrains_Mono']",
            ),
            class_name="flex justify-between items-center",
        ),
        # Report type tabs
        rx.el.div(
            report_tab_button(AppState.t["trial_balance"], "trial_balance"),
            report_tab_button(AppState.t["balance_sheet"], "balance_sheet"),
            report_tab_button(AppState.t["income_statement"], "income_statement"),
            report_tab_button(AppState.t["general_ledger"], "general_ledger"),
            class_name="flex gap-2 mb-6 border-b pb-2",
        ),
        # Report content based on selected tab
        rx.match(
            AppState.active_report_tab,
            ("trial_balance", trial_balance_report()),
            ("balance_sheet", balance_sheet_report()),
            ("income_statement", income_statement_report()),
            ("general_ledger", general_ledger_report()),
            trial_balance_report(),  # default
        ),
    )


def report_tab_button(text: str, tab_name: str) -> rx.Component:
    """Tab button for report selection."""
    return rx.el.button(
        text,
        on_click=lambda: AppState.set_active_report_tab(tab_name),
        class_name=rx.cond(
            AppState.active_report_tab == tab_name,
            "px-4 py-2 text-sm font-semibold text-emerald-600 border-b-2 border-emerald-600 font-['JetBrains_Mono']",
            "px-4 py-2 text-sm font-semibold text-gray-600 hover:text-gray-800 font-['JetBrains_Mono']",
        ),
    )


def general_ledger_row(entry: rx.Var[dict]) -> rx.Component:
    """Display a single general ledger entry row."""
    return rx.el.div(
        rx.el.p(entry["date"], class_name="col-span-2"),
        rx.el.p(entry["description"], class_name="col-span-4 truncate"),
        rx.el.p(
            entry["debit"],
            class_name="col-span-2 text-right font-mono",
        ),
        rx.el.p(
            entry["credit"],
            class_name="col-span-2 text-right font-mono",
        ),
        rx.el.p(
            entry["running_balance"],
            class_name="col-span-2 text-right font-mono font-semibold",
        ),
        class_name="grid grid-cols-12 gap-4 p-3 border-b border-gray-200 text-sm font-['JetBrains_Mono'] hover:bg-gray-50",
    )


def trial_balance_row(acc: rx.Var[dict]) -> rx.Component:
    """Display a single trial balance row."""
    return rx.el.div(
        rx.el.p(acc["code"], class_name="col-span-2"),
        rx.el.p(acc["name"], class_name="col-span-4"),
        rx.el.p(
            acc["debit"],
            class_name="col-span-2 text-right font-mono",
        ),
        rx.el.p(
            acc["credit"],
            class_name="col-span-2 text-right font-mono",
        ),
        class_name="grid grid-cols-10 gap-4 p-3 border-b border-gray-200 text-sm font-['JetBrains_Mono'] hover:bg-gray-50",
    )


def report_date_filter() -> rx.Component:
    """Date filter for reports."""
    return rx.el.div(
        rx.el.div(
            form_field(
                AppState.t["as_of_date"],
                rx.el.input(
                    type="date",
                    value=AppState.report_date,
                    on_change=AppState.set_report_date,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-['JetBrains_Mono']",
                ),
            ),
            class_name="w-64",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("download", class_name="w-4 h-4 mr-2"),
                AppState.t["export_csv"],
                on_click=AppState.export_report_csv,
                class_name="px-4 py-2 text-sm font-medium text-white bg-emerald-600 rounded-md shadow-sm hover:bg-emerald-700 flex items-center font-['JetBrains_Mono']",
            ),
            rx.el.button(
                rx.icon("printer", class_name="w-4 h-4 mr-2"),
                AppState.t["print"],
                on_click=rx.call_script("window.print()"),
                class_name="ml-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 flex items-center font-['JetBrains_Mono']",
            ),
        ),
        class_name="flex justify-between items-end mb-6 p-4 bg-gray-50 rounded-lg",
    )


def trial_balance_report() -> rx.Component:
    """Trial Balance report showing all accounts with their balances."""
    return rx.el.div(
        report_date_filter(),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    AppState.t["trial_balance"],
                    class_name="text-lg font-semibold text-center mb-2",
                ),
                rx.el.p(
                    f"{AppState.t['as_of']} {AppState.report_date}",
                    class_name="text-sm text-gray-600 text-center mb-4",
                ),
                class_name="border-b pb-4",
            ),
            # Table header
            rx.el.div(
                rx.el.p(
                    AppState.t["account_code"],
                    class_name="font-semibold col-span-2",
                ),
                rx.el.p(
                    AppState.t["account_name"],
                    class_name="font-semibold col-span-4",
                ),
                rx.el.p(
                    AppState.t["debit"],
                    class_name="font-semibold col-span-2 text-right",
                ),
                rx.el.p(
                    AppState.t["credit"],
                    class_name="font-semibold col-span-2 text-right",
                ),
                class_name="grid grid-cols-10 gap-4 p-3 bg-gray-100 rounded-t-lg text-sm font-['JetBrains_Mono']",
            ),
            # Account rows
            rx.foreach(
                AppState.trial_balance_data,
                trial_balance_row,
            ),
            # Totals row
            rx.el.div(
                rx.el.p("", class_name="col-span-2"),
                rx.el.p(
                    AppState.t["total"],
                    class_name="col-span-4 font-bold",
                ),
                rx.el.p(
                    f"${AppState.trial_balance_total_debits.to_string()}",
                    class_name="col-span-2 text-right font-mono font-bold",
                ),
                rx.el.p(
                    f"${AppState.trial_balance_total_credits.to_string()}",
                    class_name="col-span-2 text-right font-mono font-bold",
                ),
                class_name="grid grid-cols-10 gap-4 p-3 bg-emerald-50 text-sm font-['JetBrains_Mono'] border-t-2 border-emerald-600",
            ),
            class_name="bg-white rounded-lg shadow-md border border-gray-200",
        ),
    )


def balance_sheet_report() -> rx.Component:
    """Balance Sheet report showing Assets, Liabilities, and Equity."""
    return rx.el.div(
        report_date_filter(),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    AppState.t["balance_sheet"],
                    class_name="text-lg font-semibold text-center mb-2",
                ),
                rx.el.p(
                    f"{AppState.t['as_of']} {AppState.report_date}",
                    class_name="text-sm text-gray-600 text-center mb-4",
                ),
                class_name="border-b pb-4",
            ),
            # Assets Section
            rx.el.div(
                rx.el.h4(
                    AppState.t["assets"],
                    class_name="text-md font-bold text-emerald-700 mb-3 uppercase",
                ),
                rx.foreach(
                    AppState.balance_sheet_assets,
                    lambda acc: rx.el.div(
                        rx.el.p(
                            f"{acc['code']} - {acc['name']}",
                            class_name="col-span-3",
                        ),
                        rx.el.p(
                            f"${acc['balance'].to_string()}",
                            class_name="text-right font-mono",
                        ),
                        class_name="grid grid-cols-4 gap-4 px-4 py-2 text-sm font-['JetBrains_Mono']",
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        AppState.t["total_assets"],
                        class_name="col-span-3 font-bold",
                    ),
                    rx.el.p(
                        f"${AppState.total_assets.to_string()}",
                        class_name="text-right font-mono font-bold",
                    ),
                    class_name="grid grid-cols-4 gap-4 px-4 py-2 mt-2 bg-emerald-50 text-sm font-['JetBrains_Mono'] border-t border-emerald-200",
                ),
                class_name="mb-6",
            ),
            # Liabilities Section
            rx.el.div(
                rx.el.h4(
                    AppState.t["liabilities"],
                    class_name="text-md font-bold text-emerald-700 mb-3 uppercase",
                ),
                rx.foreach(
                    AppState.balance_sheet_liabilities,
                    lambda acc: rx.el.div(
                        rx.el.p(
                            f"{acc['code']} - {acc['name']}",
                            class_name="col-span-3",
                        ),
                        rx.el.p(
                            f"${abs(acc['balance']).to_string()}",
                            class_name="text-right font-mono",
                        ),
                        class_name="grid grid-cols-4 gap-4 px-4 py-2 text-sm font-['JetBrains_Mono']",
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        AppState.t["total_liabilities"],
                        class_name="col-span-3 font-bold",
                    ),
                    rx.el.p(
                        f"${AppState.total_liabilities.to_string()}",
                        class_name="text-right font-mono font-bold",
                    ),
                    class_name="grid grid-cols-4 gap-4 px-4 py-2 mt-2 bg-emerald-50 text-sm font-['JetBrains_Mono'] border-t border-emerald-200",
                ),
                class_name="mb-6",
            ),
            # Equity Section
            rx.el.div(
                rx.el.h4(
                    AppState.t["equity"],
                    class_name="text-md font-bold text-emerald-700 mb-3 uppercase",
                ),
                rx.foreach(
                    AppState.balance_sheet_equity,
                    lambda acc: rx.el.div(
                        rx.el.p(
                            f"{acc['code']} - {acc['name']}",
                            class_name="col-span-3",
                        ),
                        rx.el.p(
                            f"${abs(acc['balance']).to_string()}",
                            class_name="text-right font-mono",
                        ),
                        class_name="grid grid-cols-4 gap-4 px-4 py-2 text-sm font-['JetBrains_Mono']",
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        AppState.t["total_equity"],
                        class_name="col-span-3 font-bold",
                    ),
                    rx.el.p(
                        f"${AppState.total_equity.to_string()}",
                        class_name="text-right font-mono font-bold",
                    ),
                    class_name="grid grid-cols-4 gap-4 px-4 py-2 mt-2 bg-emerald-50 text-sm font-['JetBrains_Mono'] border-t border-emerald-200",
                ),
                class_name="mb-6",
            ),
            # Total Liabilities + Equity
            rx.el.div(
                rx.el.p(
                    AppState.t["total_liabilities_equity"],
                    class_name="col-span-3 font-bold text-lg",
                ),
                rx.el.p(
                    f"${AppState.total_liabilities_equity.to_string()}",
                    class_name="text-right font-mono font-bold text-lg",
                ),
                class_name="grid grid-cols-4 gap-4 px-4 py-3 bg-emerald-100 text-sm font-['JetBrains_Mono'] border-t-2 border-emerald-600",
            ),
            class_name="bg-white rounded-lg shadow-md border border-gray-200 p-6",
        ),
    )


def income_statement_report() -> rx.Component:
    """Income Statement report showing Revenue and Expenses."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                form_field(
                    AppState.t["start_date"],
                    rx.el.input(
                        type="date",
                        value=AppState.report_start_date,
                        on_change=AppState.set_report_start_date,
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-['JetBrains_Mono']",
                    ),
                ),
                form_field(
                    AppState.t["end_date"],
                    rx.el.input(
                        type="date",
                        value=AppState.report_end_date,
                        on_change=AppState.set_report_end_date,
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-['JetBrains_Mono']",
                    ),
                ),
                class_name="grid grid-cols-2 gap-4",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("download", class_name="w-4 h-4 mr-2"),
                    AppState.t["export_csv"],
                    on_click=AppState.export_report_csv,
                    class_name="px-4 py-2 text-sm font-medium text-white bg-emerald-600 rounded-md shadow-sm hover:bg-emerald-700 flex items-center font-['JetBrains_Mono']",
                ),
                rx.el.button(
                    rx.icon("printer", class_name="w-4 h-4 mr-2"),
                    AppState.t["print"],
                    on_click=rx.call_script("window.print()"),
                    class_name="ml-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 flex items-center font-['JetBrains_Mono']",
                ),
            ),
            class_name="flex justify-between items-end mb-6 p-4 bg-gray-50 rounded-lg",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    AppState.t["income_statement"],
                    class_name="text-lg font-semibold text-center mb-2",
                ),
                rx.el.p(
                    f"{AppState.report_start_date} {AppState.t['to']} {AppState.report_end_date}",
                    class_name="text-sm text-gray-600 text-center mb-4",
                ),
                class_name="border-b pb-4",
            ),
            # Revenue Section
            rx.el.div(
                rx.el.h4(
                    AppState.t["revenue"],
                    class_name="text-md font-bold text-emerald-700 mb-3 uppercase",
                ),
                rx.foreach(
                    AppState.income_statement_revenue,
                    lambda acc: rx.el.div(
                        rx.el.p(
                            f"{acc['code']} - {acc['name']}",
                            class_name="col-span-3",
                        ),
                        rx.el.p(
                            f"${abs(acc['balance']).to_string()}",
                            class_name="text-right font-mono",
                        ),
                        class_name="grid grid-cols-4 gap-4 px-4 py-2 text-sm font-['JetBrains_Mono']",
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        AppState.t["total_revenue"],
                        class_name="col-span-3 font-bold",
                    ),
                    rx.el.p(
                        f"${AppState.total_revenue.to_string()}",
                        class_name="text-right font-mono font-bold",
                    ),
                    class_name="grid grid-cols-4 gap-4 px-4 py-2 mt-2 bg-emerald-50 text-sm font-['JetBrains_Mono'] border-t border-emerald-200",
                ),
                class_name="mb-6",
            ),
            # Expenses Section
            rx.el.div(
                rx.el.h4(
                    AppState.t["expenses"],
                    class_name="text-md font-bold text-red-700 mb-3 uppercase",
                ),
                rx.foreach(
                    AppState.income_statement_expenses,
                    lambda acc: rx.el.div(
                        rx.el.p(
                            f"{acc['code']} - {acc['name']}",
                            class_name="col-span-3",
                        ),
                        rx.el.p(
                            f"${acc['balance'].to_string()}",
                            class_name="text-right font-mono",
                        ),
                        class_name="grid grid-cols-4 gap-4 px-4 py-2 text-sm font-['JetBrains_Mono']",
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        AppState.t["total_expenses"],
                        class_name="col-span-3 font-bold",
                    ),
                    rx.el.p(
                        f"${AppState.total_expenses.to_string()}",
                        class_name="text-right font-mono font-bold",
                    ),
                    class_name="grid grid-cols-4 gap-4 px-4 py-2 mt-2 bg-red-50 text-sm font-['JetBrains_Mono'] border-t border-red-200",
                ),
                class_name="mb-6",
            ),
            # Net Income
            rx.el.div(
                rx.el.p(
                    AppState.t["net_income"],
                    class_name="col-span-3 font-bold text-lg",
                ),
                rx.el.p(
                    f"${AppState.net_income.to_string()}",
                    class_name=rx.cond(
                        AppState.net_income >= 0,
                        "text-right font-mono font-bold text-lg text-emerald-600",
                        "text-right font-mono font-bold text-lg text-red-600",
                    ),
                ),
                class_name="grid grid-cols-4 gap-4 px-4 py-3 bg-gray-100 text-sm font-['JetBrains_Mono'] border-t-2 border-gray-600",
            ),
            class_name="bg-white rounded-lg shadow-md border border-gray-200 p-6",
        ),
    )


def general_ledger_report() -> rx.Component:
    """General Ledger report showing all transactions by account."""
    return rx.el.div(
        rx.el.div(
            form_field(
                AppState.t["select_account"],
                rx.el.select(
                    rx.el.option(AppState.t["all_accounts"], value=""),
                    rx.foreach(
                        AppState.accounts,
                        lambda acc: rx.el.option(
                            f"{acc['code']} - {acc['name']}", value=acc["id"]
                        ),
                    ),
                    value=AppState.general_ledger_account_id,
                    on_change=AppState.set_general_ledger_account_id,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-['JetBrains_Mono'] bg-white",
                ),
            ),
            class_name="mb-6 p-4 bg-gray-50 rounded-lg",
        ),
        rx.cond(
            AppState.general_ledger_account_id != "",
            rx.el.div(
                # Header
                rx.el.div(
                    rx.el.p(
                        AppState.t["date"],
                        class_name="font-semibold col-span-2",
                    ),
                    rx.el.p(
                        AppState.t["description"],
                        class_name="font-semibold col-span-4",
                    ),
                    rx.el.p(
                        AppState.t["debit"],
                        class_name="font-semibold col-span-2 text-right",
                    ),
                    rx.el.p(
                        AppState.t["credit"],
                        class_name="font-semibold col-span-2 text-right",
                    ),
                    rx.el.p(
                        AppState.t["balance"],
                        class_name="font-semibold col-span-2 text-right",
                    ),
                    class_name="grid grid-cols-12 gap-4 p-3 bg-gray-100 rounded-t-lg text-sm font-['JetBrains_Mono']",
                ),
                # Transaction entries
                rx.foreach(
                    AppState.general_ledger_entries,
                    general_ledger_row,
                ),
                class_name="bg-white rounded-lg shadow-md border border-gray-200",
            ),
            rx.el.div(
                rx.el.p(
                    AppState.t["select_account_prompt"],
                    class_name="text-center text-gray-500 py-12",
                ),
                class_name="bg-white rounded-lg shadow-md border border-gray-200",
            ),
        ),
    )


