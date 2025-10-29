import reflex as rx
from app.state import AppState
from app.components import (
    account_form,
    transaction_form,
    account_card,
    fab_button,
    transaction_list_view,
)
from app.settings import settings_modal
from app.reports import reports_view
from app.dashboard import dashboard_view


def tab_button(text: str, tab_name: str) -> rx.Component:
    return rx.el.button(
        text,
        on_click=lambda: AppState.set_active_tab(tab_name),
        data_tab=tab_name,
        class_name=rx.cond(
            AppState.active_tab == tab_name,
            "px-4 py-2 text-sm font-semibold text-white bg-emerald-600 rounded-md shadow-sm transition-all duration-200",
            "px-4 py-2 text-sm font-semibold text-gray-600 hover:bg-gray-200 rounded-md transition-all duration-200",
        ),
    )


def chart_of_accounts_view() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            AppState.t["chart_of_accounts"],
            class_name="text-xl font-semibold text-gray-700 mb-6 font-['JetBrains_Mono']",
        ),
        rx.el.div(
            rx.foreach(AppState.accounts, account_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
        ),
    )


def index() -> rx.Component:
    return rx.el.main(
        # Keyboard shortcuts
        rx.el.script("""
            document.addEventListener('keydown', function(e) {
                // Ctrl/Cmd + N - New Account
                if ((e.ctrlKey || e.metaKey) && e.key === 'n' && !e.shiftKey) {
                    e.preventDefault();
                    // Trigger account form toggle
                    const accountButton = document.querySelector('[data-shortcut="new-account"]');
                    if (accountButton) accountButton.click();
                }
                // Ctrl/Cmd + Shift + N - New Transaction
                if ((e.ctrlKey || e.metaKey) && e.key === 'N' && e.shiftKey) {
                    e.preventDefault();
                    // Trigger transaction form toggle
                    const transactionButton = document.querySelector('[data-shortcut="new-transaction"]');
                    if (transactionButton) transactionButton.click();
                }
                // Ctrl/Cmd + , - Settings
                if ((e.ctrlKey || e.metaKey) && e.key === ',') {
                    e.preventDefault();
                    const settingsButton = document.querySelector('[data-shortcut="settings"]');
                    if (settingsButton) settingsButton.click();
                }
                // Ctrl/Cmd + D - Dashboard
                if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
                    e.preventDefault();
                    const dashboardTab = document.querySelector('[data-tab="dashboard"]');
                    if (dashboardTab) dashboardTab.click();
                }
            });
        """),
        rx.el.div(
            rx.el.header(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            AppState.t["app_title"],
                            class_name="text-2xl font-bold text-gray-800 font-['JetBrains_Mono']",
                        ),
                        rx.el.p(
                            AppState.t["app_subtitle"],
                            class_name="text-sm text-gray-500 font-['JetBrains_Mono']",
                        ),
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon("circle", class_name="w-3 h-3 text-green-500"),
                            rx.el.p(
                                AppState.t["online"], class_name="text-sm font-medium"
                            ),
                            class_name="flex items-center gap-2 px-3 py-1 bg-green-100/50 rounded-full",
                        ),
                        rx.el.select(
                            rx.foreach(
                                AppState.available_languages,
                                lambda lang: rx.el.option(
                                    f"{lang['flag']} {lang['name']}", value=lang["code"]
                                ),
                            ),
                            value=AppState.language,
                            on_change=AppState.set_language,
                            class_name="px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-['JetBrains_Mono'] bg-white",
                        ),
                        tab_button(AppState.t["dashboard"], "dashboard"),
                        tab_button(AppState.t["chart_of_accounts"], "accounts"),
                        tab_button(AppState.t["transactions"], "transactions"),
                        tab_button(AppState.t["reports"], "reports"),
                        rx.el.button(
                            rx.cond(
                                AppState.is_dark_mode,
                                rx.icon("sun", class_name="w-5 h-5"),
                                rx.icon("moon", class_name="w-5 h-5"),
                            ),
                            on_click=AppState.toggle_dark_mode,
                            class_name="p-2 text-gray-600 hover:bg-gray-200 rounded-full transition-colors",
                        ),
                        rx.el.button(
                            rx.icon("settings", class_name="w-5 h-5"),
                            on_click=AppState.toggle_settings,
                            data_shortcut="settings",
                            class_name="p-2 text-gray-600 hover:bg-gray-200 rounded-full transition-colors",
                        ),
                        class_name="flex items-center gap-4",
                    ),
                    class_name="container mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center border-b",
                ),
                class_name="bg-white/80 backdrop-blur-md sticky top-0 z-10",
            ),
            rx.el.div(
                rx.match(
                    AppState.active_tab,
                    ("dashboard", dashboard_view()),
                    ("accounts", chart_of_accounts_view()),
                    ("transactions", transaction_list_view()),
                    ("reports", reports_view()),
                    dashboard_view(),  # default
                ),
                class_name="container mx-auto px-4 sm:px-6 lg:px-8 py-8",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("user-plus", class_name="w-6 h-6"),
                    on_click=AppState.toggle_account_form,
                    data_shortcut="new-account",
                    class_name="bg-emerald-500 text-white p-4 rounded-full shadow-lg hover:bg-emerald-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-all duration-300 hover:scale-110",
                ),
                rx.el.button(
                    rx.icon("file-plus-2", class_name="w-6 h-6"),
                    on_click=AppState.toggle_transaction_form,
                    data_shortcut="new-transaction",
                    class_name="bg-emerald-500 text-white p-4 rounded-full shadow-lg hover:bg-emerald-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-all duration-300 hover:scale-110",
                ),
                class_name="fixed bottom-6 right-6 flex flex-col gap-4 z-20",
            ),
            rx.cond(AppState.show_account_form, account_form(), None),
            rx.cond(AppState.show_transaction_form, transaction_form(), None),
            rx.cond(AppState.show_settings, settings_modal(), None),
        ),
        class_name="font-['JetBrains_Mono'] bg-gray-50 min-h-screen",
    )


app = rx.App(
    theme=rx.theme(
        appearance="light",  # Default to light, dark mode toggle handled in UI
        accent_color="grass",
    ),
    head_components=[
        rx.el.script(
            src="https://cdn.jsdelivr.net/npm/pouchdb@8.0.1/dist/pouchdb.min.js"
        ),
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, on_load=AppState.load_from_storage)