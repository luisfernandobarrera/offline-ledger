import reflex as rx
from app.state import AppState


def dashboard_view() -> rx.Component:
    """Dashboard with key metrics and statistics."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                AppState.t["dashboard"],
                class_name="text-xl font-semibold text-gray-700 mb-6 font-['JetBrains_Mono']",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        # Quick stats cards
        rx.el.div(
            stat_card(
                AppState.t["total_assets"],
                f"${AppState.total_assets.to_string()}",
                "trending-up",
                "emerald",
            ),
            stat_card(
                AppState.t["total_liabilities"],
                f"${AppState.total_liabilities.to_string()}",
                "trending-down",
                "red",
            ),
            stat_card(
                AppState.t["net_worth"],
                f"${(AppState.total_assets - AppState.total_liabilities).to_string()}",
                "dollar-sign",
                "blue",
            ),
            stat_card(
                AppState.t["total_accounts"],
                AppState.accounts.length().to_string(),
                "layers",
                "purple",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
        ),
        # Income Statement Summary
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    AppState.t["income_statement"],
                    class_name="text-lg font-semibold text-gray-800 mb-4 font-['JetBrains_Mono']",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            AppState.t["total_revenue"],
                            class_name="text-sm text-gray-600",
                        ),
                        rx.el.p(
                            f"${AppState.total_revenue.to_string()}",
                            class_name="text-2xl font-bold text-emerald-600 font-['JetBrains_Mono']",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.p(
                            AppState.t["total_expenses"],
                            class_name="text-sm text-gray-600",
                        ),
                        rx.el.p(
                            f"${AppState.total_expenses.to_string()}",
                            class_name="text-2xl font-bold text-red-600 font-['JetBrains_Mono']",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.p(
                            AppState.t["net_income"],
                            class_name="text-sm text-gray-600 font-semibold",
                        ),
                        rx.el.p(
                            f"${AppState.net_income.to_string()}",
                            class_name=rx.cond(
                                AppState.net_income >= 0,
                                "text-3xl font-bold text-emerald-600 font-['JetBrains_Mono']",
                                "text-3xl font-bold text-red-600 font-['JetBrains_Mono']",
                            ),
                        ),
                        class_name="pt-4 border-t border-gray-200",
                    ),
                ),
                class_name="p-6 bg-white rounded-lg shadow-md border border-gray-200",
            ),
            # Balance Sheet Summary
            rx.el.div(
                rx.el.h3(
                    AppState.t["balance_sheet"],
                    class_name="text-lg font-semibold text-gray-800 mb-4 font-['JetBrains_Mono']",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            AppState.t["total_assets"],
                            class_name="text-sm text-gray-600",
                        ),
                        rx.el.p(
                            f"${AppState.total_assets.to_string()}",
                            class_name="text-2xl font-bold text-gray-800 font-['JetBrains_Mono']",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.p(
                            AppState.t["total_liabilities_equity"],
                            class_name="text-sm text-gray-600",
                        ),
                        rx.el.p(
                            f"${AppState.total_liabilities_equity.to_string()}",
                            class_name="text-2xl font-bold text-gray-800 font-['JetBrains_Mono']",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.p(
                            AppState.t["balance"],
                            class_name="text-sm text-gray-600 font-semibold",
                        ),
                        rx.el.p(
                            f"${(AppState.total_assets - AppState.total_liabilities_equity).to_string()}",
                            class_name=rx.cond(
                                (AppState.total_assets - AppState.total_liabilities_equity) == 0,
                                "text-3xl font-bold text-emerald-600 font-['JetBrains_Mono']",
                                "text-3xl font-bold text-red-600 font-['JetBrains_Mono']",
                            ),
                        ),
                        class_name="pt-4 border-t border-gray-200",
                    ),
                ),
                class_name="p-6 bg-white rounded-lg shadow-md border border-gray-200",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8",
        ),
        # Recent Transactions
        rx.el.div(
            rx.el.h3(
                AppState.t["transactions"],
                class_name="text-lg font-semibold text-gray-800 mb-4 font-['JetBrains_Mono']",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        AppState.t["date"],
                        class_name="font-semibold col-span-2",
                    ),
                    rx.el.p(
                        AppState.t["description"],
                        class_name="font-semibold col-span-6",
                    ),
                    rx.el.p(
                        AppState.t["amount"],
                        class_name="font-semibold col-span-2 text-right",
                    ),
                    class_name="grid grid-cols-10 items-center p-3 bg-gray-100 rounded-t-lg text-sm font-['JetBrains_Mono']",
                ),
                rx.foreach(
                    AppState.recent_transactions,
                    transaction_row,
                ),
                class_name="bg-white rounded-lg shadow-md border border-gray-200",
            ),
            class_name="mb-8",
        ),
        # Account Type Breakdown
        rx.el.div(
            rx.el.h3(
                AppState.t["chart_of_accounts"],
                class_name="text-lg font-semibold text-gray-800 mb-4 font-['JetBrains_Mono']",
            ),
            rx.el.div(
                account_type_summary(AppState.t["asset"], AppState.asset_count),
                account_type_summary(AppState.t["liability"], AppState.liability_count),
                account_type_summary(AppState.t["equity"], AppState.equity_count),
                account_type_summary(AppState.t["revenue"], AppState.revenue_count),
                account_type_summary(AppState.t["expense"], AppState.expense_count),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4",
            ),
        ),
    )


def stat_card(label: str, value: str, icon: str, color: str) -> rx.Component:
    """Display a statistic card."""
    color_classes = {
        "emerald": "bg-emerald-50 text-emerald-600",
        "red": "bg-red-50 text-red-600",
        "blue": "bg-blue-50 text-blue-600",
        "purple": "bg-purple-50 text-purple-600",
    }
    
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    label,
                    class_name="text-sm text-gray-600 font-['JetBrains_Mono']",
                ),
                rx.el.p(
                    value,
                    class_name="text-2xl font-bold text-gray-800 mt-2 font-['JetBrains_Mono']",
                ),
            ),
            rx.el.div(
                rx.icon(icon, class_name="w-8 h-8"),
                class_name=f"p-3 rounded-lg {color_classes.get(color, 'bg-gray-50 text-gray-600')}",
            ),
            class_name="flex justify-between items-start",
        ),
        class_name="p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 border border-gray-200",
    )


def transaction_row(txn: rx.Var[dict]) -> rx.Component:
    """Display a single transaction row."""
    # Calculate total inline by formatting the entries
    return rx.el.div(
        rx.el.p(txn["date"], class_name="col-span-2"),
        rx.el.p(txn["description"], class_name="col-span-6 truncate"),
        rx.el.p(
            # Simply show a placeholder for now - amounts are complex to calculate in JS
            "-",
            class_name="col-span-2 text-right font-mono",
        ),
        class_name="grid grid-cols-10 items-center p-3 border-b border-gray-100 hover:bg-gray-50 text-sm font-['JetBrains_Mono']",
    )


def account_type_summary(type_label: str, count: rx.Var[int]) -> rx.Component:
    """Display summary for an account type."""
    return rx.el.div(
        rx.el.p(
            type_label,
            class_name="text-sm font-semibold text-gray-700 mb-2 uppercase font-['JetBrains_Mono']",
        ),
        rx.el.p(
            count,
            class_name="text-3xl font-bold text-emerald-600 font-['JetBrains_Mono']",
        ),
        rx.el.p(
            "accounts",
            class_name="text-xs text-gray-500 mt-1",
        ),
        class_name="p-4 bg-white rounded-lg shadow-md border border-gray-200 hover:border-emerald-500 transition-colors duration-200",
    )

