import reflex as rx
from app.state import AppState
from app.components import form_field


def settings_modal() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    AppState.t["settings_title"],
                    class_name="text-lg font-bold text-gray-800 font-['JetBrains_Mono']",
                ),
                rx.el.button(
                    rx.icon("x", class_name="w-5 h-5"),
                    on_click=AppState.toggle_settings,
                    class_name="p-1 rounded-full hover:bg-gray-200",
                ),
                class_name="flex justify-between items-center pb-4 border-b",
            ),
            rx.el.div(
                rx.el.h3(
                    AppState.t["data_management"],
                    class_name="font-semibold text-gray-700 mb-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            AppState.t["export_data_title"], class_name="font-medium"
                        ),
                        rx.el.p(
                            AppState.t["export_data_desc"],
                            class_name="text-sm text-gray-500",
                        ),
                        class_name="flex-grow",
                    ),
                    rx.el.button(
                        AppState.t["export"],
                        on_click=AppState.export_data,
                        class_name="px-4 py-2 text-sm font-medium text-white bg-emerald-600 rounded-md shadow-sm hover:bg-emerald-700",
                    ),
                    class_name="flex items-center justify-between p-4 bg-gray-50 rounded-lg",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            AppState.t["import_data_title"], class_name="font-medium"
                        ),
                        rx.el.p(
                            AppState.t["import_data_desc"],
                            class_name="text-sm text-gray-500",
                        ),
                        class_name="flex-grow",
                    ),
                    rx.upload.root(
                        rx.el.button(
                            AppState.t["import"],
                            class_name="px-4 py-2 text-sm font-medium text-white bg-emerald-600 rounded-md shadow-sm hover:bg-emerald-700",
                        ),
                        id="import-upload",
                        on_drop=AppState.import_data,
                        class_name="flex items-center justify-center",
                    ),
                    class_name="flex items-center justify-between p-4 bg-gray-50 rounded-lg mt-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            AppState.t["clear_data_title"],
                            class_name="font-medium text-red-600",
                        ),
                        rx.el.p(
                            AppState.t["clear_data_desc"],
                            class_name="text-sm text-gray-500",
                        ),
                        class_name="flex-grow",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Normalize Data",
                            on_click=AppState.normalize_data,
                            class_name="px-3 py-2 text-sm font-medium text-white bg-emerald-600 rounded-md shadow-sm hover:bg-emerald-700 mr-2",
                        ),
                        rx.el.button(
                            "Recompute Balances",
                            on_click=AppState.recompute_balances_from_transactions,
                            class_name="px-3 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md shadow-sm hover:bg-indigo-700",
                        ),
                    ),
                    rx.radix.primitives.dialog.root(
                        rx.radix.primitives.dialog.trigger(
                            rx.el.button(
                                AppState.t["clear_data"],
                                class_name="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md shadow-sm hover:bg-red-700",
                            )
                        ),
                        rx.radix.primitives.dialog.portal(
                            rx.radix.primitives.dialog.overlay(
                                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-[51]"
                            ),
                            rx.radix.primitives.dialog.content(
                                rx.radix.primitives.dialog.title(
                                    AppState.t["confirm_deletion_title"],
                                    class_name="text-lg font-semibold text-gray-800",
                                ),
                                rx.radix.primitives.dialog.description(
                                    AppState.t["confirm_deletion_desc"],
                                    class_name="text-sm text-gray-600 mt-2",
                                ),
                                rx.el.div(
                                    rx.radix.primitives.dialog.close(
                                        rx.el.button(
                                            AppState.t["cancel"],
                                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md shadow-sm hover:bg-gray-200",
                                        )
                                    ),
                                    rx.radix.primitives.dialog.close(
                                        rx.el.button(
                                            AppState.t["clear_data"],
                                            on_click=AppState.clear_all_data,
                                            class_name="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md shadow-sm hover:bg-red-700",
                                        )
                                    ),
                                    class_name="flex justify-end gap-4 mt-6",
                                ),
                                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-lg shadow-xl p-6 w-full max-w-sm z-[52]",
                            ),
                        ),
                    ),
                    class_name="flex items-center justify-between p-4 border border-red-200 bg-red-50 rounded-lg mt-4",
                ),
                class_name="py-6",
            ),
            class_name="p-8 bg-white rounded-lg shadow-2xl w-full max-w-lg",
        ),
        class_name="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4",
    )