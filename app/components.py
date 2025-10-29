import reflex as rx
from app.state import AppState


def transaction_list_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                AppState.t["transactions_title"],
                class_name="text-xl font-semibold text-gray-700 font-['JetBrains_Mono']",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        filter_panel(),
        rx.el.div(
            rx.el.div(
                rx.el.p(AppState.t["date"], class_name="font-semibold col-span-2"),
                rx.el.p(
                    AppState.t["description"], class_name="font-semibold col-span-5"
                ),
                rx.el.p(
                    AppState.t["amount"],
                    class_name="font-semibold col-span-2 text-right",
                ),
                class_name="grid grid-cols-10 items-center p-2 text-sm text-gray-600 bg-gray-100 rounded-t-lg font-['JetBrains_Mono']",
            ),
            rx.el.div(
                rx.el.span(
                    AppState.filtered_count_badge,
                    class_name="text-xs text-gray-500 px-2",
                ),
                class_name="mt-1",
            ),
            rx.cond(
                AppState.filtered_transaction_count == 0,
                rx.el.div(
                    rx.el.p(
                        "No transactions match your filters.",
                        class_name="text-sm text-gray-600",
                    ),
                    rx.el.button(
                        "Reset filters",
                        on_click=AppState.reset_filters,
                        class_name="mt-2 px-3 py-1 text-sm text-white bg-gray-600 rounded-md",
                    ),
                    class_name="bg-white rounded-lg shadow-md border border-gray-200 mt-6 p-6 text-center",
                ),
                rx.el.div(
                    rx.foreach(AppState.filtered_transactions_rows, transaction_list_item),
                    class_name="bg-white rounded-lg shadow-md border border-gray-200 mt-6",
                ),
            ),
        ),
    )


def filter_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                form_field(
                    AppState.t["start_date"],
                    rx.el.input(
                        type="date",
                        default_value=AppState.filter_start_date,
                        on_change=AppState.set_filter_start_date,
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-['JetBrains_Mono']",
                    ),
                ),
                form_field(
                    AppState.t["end_date"],
                    rx.el.input(
                        type="date",
                        default_value=AppState.filter_end_date,
                        on_change=AppState.set_filter_end_date,
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-['JetBrains_Mono']",
                    ),
                ),
                class_name="grid md:grid-cols-2 gap-4",
            ),
            rx.el.div(
                rx.el.button(
                    AppState.t["today"],
                    on_click=lambda: AppState.set_date_filter_preset("today"),
                    class_name="px-3 py-1 text-xs font-medium text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200",
                ),
                rx.el.button(
                    AppState.t["this_week"],
                    on_click=lambda: AppState.set_date_filter_preset("this_week"),
                    class_name="px-3 py-1 text-xs font-medium text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200",
                ),
                rx.el.button(
                    AppState.t["this_month"],
                    on_click=lambda: AppState.set_date_filter_preset("this_month"),
                    class_name="px-3 py-1 text-xs font-medium text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200",
                ),
                rx.el.button(
                    AppState.t["this_year"],
                    on_click=lambda: AppState.set_date_filter_preset("this_year"),
                    class_name="px-3 py-1 text-xs font-medium text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200",
                ),
                rx.el.button(
                    AppState.t["all_time"],
                    on_click=lambda: AppState.set_date_filter_preset("all"),
                    class_name="px-3 py-1 text-xs font-medium text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200",
                ),
                class_name="flex flex-wrap gap-2 mt-2",
            ),
            class_name="col-span-1 md:col-span-2",
        ),
        form_field(
            AppState.t["description"],
            rx.el.input(
                placeholder=f"{AppState.t['search']}...",
                default_value=AppState.filter_description,
                on_change=AppState.set_filter_description.debounce(300),
                class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-['JetBrains_Mono']",
            ),
        ),
        form_field(
            AppState.t["account"],
            rx.el.select(
                rx.el.option(AppState.t["all_accounts"], value=""),
                rx.foreach(
                    AppState.accounts,
                    lambda acc: rx.el.option(
                        f"{acc['code']} - {acc['name']}", value=acc["id"]
                    ),
                ),
                default_value=AppState.filter_account_id,
                on_change=AppState.set_filter_account_id,
                class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-['JetBrains_Mono'] bg-white",
            ),
        ),
        rx.el.div(
            form_field(
                AppState.t["min_amount"],
                rx.el.input(
                    type="number",
                    placeholder="0.00",
                    default_value=AppState.filter_min_amount,
                    on_change=AppState.set_filter_min_amount,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-['JetBrains_Mono']",
                ),
            ),
            form_field(
                AppState.t["max_amount"],
                rx.el.input(
                    type="number",
                    placeholder="1000.00",
                    default_value=AppState.filter_max_amount,
                    on_change=AppState.set_filter_max_amount,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-['JetBrains_Mono']",
                ),
            ),
            class_name="grid md:grid-cols-2 gap-4",
        ),
        rx.el.button(
            AppState.t["reset_filters"],
            on_click=AppState.reset_filters,
            class_name="w-full mt-4 px-4 py-2 text-sm font-medium text-white bg-gray-600 border border-transparent rounded-md shadow-sm hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 font-['JetBrains_Mono']",
        ),
        class_name="p-4 bg-white rounded-lg shadow-md border border-gray-200 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 items-start",
    )


def transaction_list_item(transaction: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(transaction["date"], class_name="col-span-2"),
            rx.el.p(transaction["description"], class_name="col-span-5 truncate"),
            rx.el.p(
            f"${transaction['total'].to_string()}",
                class_name="col-span-2 text-right",
            ),
            rx.el.button(
                rx.icon(
                    rx.cond(
                        AppState.expanded_transaction_id == transaction["id"],
                        "chevron-up",
                        "chevron-down",
                    ),
                    class_name="w-5 h-5",
                ),
                on_click=lambda: AppState.toggle_expand_transaction(transaction["id"]),
                class_name="justify-self-end p-1 rounded-full hover:bg-gray-100",
            ),
            class_name="grid grid-cols-10 items-center p-2 cursor-pointer border-b border-gray-100 hover:bg-gray-50 font-['JetBrains_Mono'] text-sm",
        ),
        rx.cond(
            AppState.expanded_transaction_id == transaction["id"],
            transaction_detail_view(transaction),
            None,
        ),
    )


def transaction_detail_view(transaction: rx.Var[dict]) -> rx.Component:
    account_map = AppState.get_account_map
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                AppState.t["account"],
                class_name="font-semibold text-xs uppercase col-span-5 text-gray-500",
            ),
            rx.el.p(
                AppState.t["debit"],
                class_name="font-semibold text-xs uppercase col-span-2 text-right text-gray-500",
            ),
            rx.el.p(
                AppState.t["credit"],
                class_name="font-semibold text-xs uppercase col-span-2 text-right text-gray-500",
            ),
            class_name="grid grid-cols-9 items-center px-4 pt-2",
        ),
        rx.foreach(
            AppState.entries_for_expanded,
            lambda entry: rx.el.div(
                rx.el.div(
                    rx.el.p(
                        f"{account_map[entry['account_id']]['code']} - {account_map[entry['account_id']]['name']}"
                    ),
                    rx.el.span(
                        account_map[entry["account_id"]]["type"],
                        class_name="text-xs text-gray-500",
                    ),
                    class_name="col-span-5",
                ),
                rx.el.p(
                    f"{entry['debit'].to_string()}",
                    class_name="col-span-2 text-right font-mono",
                ),
                rx.el.p(
                    f"{entry['credit'].to_string()}",
                    class_name="col-span-2 text-right font-mono",
                ),
                class_name="grid grid-cols-9 items-center p-4 border-b border-gray-100",
            ),
        ),
        class_name="bg-gray-50 p-4 font-['JetBrains_Mono'] text-sm",
    )


def form_field(
    label: str, component: rx.Component, error_message: rx.Var[str] | None = None
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            class_name="text-sm font-medium text-gray-700 font-['JetBrains_Mono']",
        ),
        component,
        rx.cond(
            error_message,
            rx.el.p(
                error_message,
                class_name="text-xs text-red-500 mt-1 font-['JetBrains_Mono']",
            ),
            None,
        ),
        class_name="flex flex-col gap-1 w-full",
    )


def account_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    AppState.t["new_account_title"],
                    class_name="text-lg font-bold text-gray-800 font-['JetBrains_Mono']",
                ),
                rx.el.button(
                    rx.icon("x", class_name="w-5 h-5"),
                    on_click=AppState.toggle_account_form,
                    class_name="p-1 rounded-full hover:bg-gray-200",
                ),
                class_name="flex justify-between items-center mb-6 pb-4 border-b",
            ),
            form_field(
                AppState.t["account_name"],
                rx.el.input(
                    placeholder=AppState.t["account_name_placeholder"],
                    default_value=AppState.new_account_name,
                    on_change=AppState.set_new_account_name,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-['JetBrains_Mono']",
                ),
                AppState.account_name_error,
            ),
            form_field(
                AppState.t["account_code"],
                rx.el.input(
                    placeholder=AppState.t["account_code_placeholder"],
                    default_value=AppState.new_account_code,
                    on_change=AppState.set_new_account_code,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-['JetBrains_Mono']",
                ),
                AppState.account_code_error,
            ),
            form_field(
                AppState.t["account_type"],
                rx.el.select(
                    rx.foreach(
                        AppState.account_types,
                        lambda type: rx.el.option(AppState.t[type.lower()], value=type),
                    ),
                    value=AppState.new_account_type,
                    on_change=AppState.set_new_account_type,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-['JetBrains_Mono'] bg-white",
                ),
            ),
            rx.el.div(
                rx.el.button(
                    AppState.t["cancel"],
                    on_click=AppState.toggle_account_form,
                    class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md shadow-sm hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 font-['JetBrains_Mono']",
                ),
                rx.el.button(
                    AppState.t["create_account"],
                    on_click=AppState.create_account,
                    disabled=rx.cond(AppState.is_account_form_valid, False, True),
                    class_name="px-4 py-2 text-sm font-medium text-white bg-emerald-600 border border-transparent rounded-md shadow-sm hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed font-['JetBrains_Mono']",
                ),
                class_name="flex justify-end gap-4 mt-8",
            ),
            class_name="p-8 bg-white rounded-lg shadow-2xl w-full max-w-md",
        ),
        class_name="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4",
    )


def transaction_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        AppState.t["new_transaction_title"],
                        class_name="text-lg font-bold text-gray-800 font-['JetBrains_Mono']",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="w-5 h-5"),
                        on_click=AppState.toggle_transaction_form,
                        class_name="p-1 rounded-full hover:bg-gray-200",
                    ),
                    class_name="flex justify-between items-center mb-6 pb-4 border-b",
                ),
                rx.el.div(
                    form_field(
                        AppState.t["date"],
                        rx.el.input(
                            type="date",
                            default_value=AppState.new_transaction_date,
                            on_change=AppState.set_new_transaction_date,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-['JetBrains_Mono']",
                        ),
                    ),
                    form_field(
                        AppState.t["description"],
                        rx.el.input(
                            placeholder=AppState.t["description_placeholder"],
                            default_value=AppState.new_transaction_description,
                            on_change=AppState.set_new_transaction_description,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-['JetBrains_Mono']",
                        ),
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6",
                ),
                rx.el.div(
                    rx.el.p(
                        AppState.t["account"],
                        class_name="text-xs font-bold text-gray-500 uppercase col-span-4",
                    ),
                    rx.el.p(
                        AppState.t["debit"],
                        class_name="text-xs font-bold text-gray-500 uppercase text-right col-span-2",
                    ),
                    rx.el.p(
                        AppState.t["credit"],
                        class_name="text-xs font-bold text-gray-500 uppercase text-right col-span-2",
                    ),
                    rx.el.div(),
                    class_name="grid grid-cols-9 gap-x-4 items-center px-2 pb-2 mb-2 border-b",
                ),
                rx.foreach(
                    AppState.new_transaction_entries,
                    lambda entry, index: rx.el.div(
                        rx.el.select(
                            rx.el.option(
                                AppState.t["select_account"], value="", disabled=True
                            ),
                            rx.foreach(
                                AppState.accounts,
                                lambda acc: rx.el.option(
                                    f"{acc['code']} - {acc['name']}", value=acc["id"]
                                ),
                            ),
                            on_change=lambda val: AppState.update_entry(
                                index, "account_id", val
                            ),
                            value=entry["account_id"].to(str),
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-['JetBrains_Mono'] bg-white col-span-4",
                        ),
                        rx.el.input(
                            type="number",
                            placeholder="0.00",
                            on_change=lambda val: AppState.update_entry(
                                index, "debit", val
                            ),
                            default_value=entry["debit"].to_string(),
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 text-right font-['JetBrains_Mono'] col-span-2",
                        ),
                        rx.el.input(
                            type="number",
                            placeholder="0.00",
                            on_change=lambda val: AppState.update_entry(
                                index, "credit", val
                            ),
                            default_value=entry["credit"].to_string(),
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 text-right font-['JetBrains_Mono'] col-span-2",
                        ),
                        rx.el.button(
                            rx.icon("trash-2", class_name="w-4 h-4 text-gray-500"),
                            on_click=lambda: AppState.remove_entry_row(index),
                            disabled=AppState.new_transaction_entries.length() <= 2,
                            class_name="p-2 rounded-md hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed justify-self-center",
                        ),
                        class_name="grid grid-cols-9 gap-x-4 items-center mb-2",
                    ),
                ),
                rx.el.button(
                    rx.icon("plus", class_name="w-4 h-4 mr-2"),
                    AppState.t["add_row"],
                    on_click=AppState.add_entry_row,
                    class_name="mt-2 px-3 py-1 text-sm text-emerald-600 font-medium flex items-center hover:bg-emerald-50 rounded-md font-['JetBrains_Mono']",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(f"{AppState.t['debits']}:", class_name="font-semibold"),
                        rx.el.p(
                            f"${AppState.total_debits.to_string()}",
                            class_name="font-mono",
                        ),
                        class_name="flex justify-between",
                    ),
                    rx.el.div(
                        rx.el.p(
                            f"{AppState.t['credits']}:", class_name="font-semibold"
                        ),
                        rx.el.p(
                            f"${AppState.total_credits.to_string()}",
                            class_name="font-mono",
                        ),
                        class_name="flex justify-between",
                    ),
                    rx.el.div(
                        rx.el.p(
                            f"{AppState.t['balance']}:", class_name="font-semibold"
                        ),
                        rx.el.p(
                            f"${AppState.transaction_balance.to_string()}",
                            class_name=rx.cond(
                                AppState.transaction_balance == 0,
                                "font-mono text-green-600",
                                "font-mono text-red-600",
                            ),
                        ),
                        class_name="flex justify-between pt-2 border-t mt-2",
                    ),
                    class_name="mt-6 p-4 bg-gray-50 rounded-lg text-sm font-['JetBrains_Mono']",
                ),
                rx.el.div(
                    rx.el.button(
                        AppState.t["cancel"],
                        on_click=AppState.toggle_transaction_form,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md shadow-sm hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 font-['JetBrains_Mono']",
                    ),
                    rx.el.button(
                        AppState.t["create_transaction"],
                        on_click=AppState.create_transaction,
                    disabled=rx.cond(AppState.is_transaction_form_valid, False, True),
                        class_name="px-4 py-2 text-sm font-medium text-white bg-emerald-600 border border-transparent rounded-md shadow-sm hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed font-['JetBrains_Mono']",
                    ),
                    class_name="flex justify-end gap-4 mt-8",
                ),
                class_name="p-8 bg-white rounded-lg shadow-2xl w-full max-w-4xl",
            ),
            class_name="max-h-[90vh] overflow-y-auto",
        ),
        class_name="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4",
    )


def account_card(account: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                account["code"],
                class_name="text-sm font-bold text-gray-800 font-['JetBrains_Mono']",
            ),
            rx.el.span(
                AppState.t[account["type"].to(str).lower()],
                class_name="px-2 py-0.5 text-xs font-semibold rounded-full bg-emerald-100 text-emerald-800 font-['JetBrains_Mono']",
            ),
            class_name="flex justify-between items-center mb-2",
        ),
        rx.el.p(
            account["name"],
            class_name="text-base font-medium text-gray-600 mb-4 font-['JetBrains_Mono']",
        ),
        rx.el.div(
            rx.el.p(
                AppState.t["balance"],
                class_name="text-sm text-gray-500 font-['JetBrains_Mono']",
            ),
            rx.el.p(
                f"${account['balance'].to_string()}",
                class_name="text-lg font-bold text-gray-900 font-['JetBrains_Mono']",
            ),
            class_name="text-right",
        ),
        class_name="bg-white p-4 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 border border-gray-200",
    )


def fab_button(
    icon_name: str, on_click_event: rx.event.EventHandler, tooltip_text: str
) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon(icon_name, class_name="w-6 h-6"),
            on_click=on_click_event,
            class_name="bg-emerald-500 text-white p-4 rounded-full shadow-lg hover:bg-emerald-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-all duration-300",
        ),
        class_name="group relative",
    )