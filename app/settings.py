import reflex as rx
from app.state import AppState
from app.components import form_field


def settings_modal() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Settings",
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
                    "Data Management", class_name="font-semibold text-gray-700 mb-2"
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Export Data", class_name="font-medium"),
                        rx.el.p(
                            "Download all accounts and transactions as a JSON file.",
                            class_name="text-sm text-gray-500",
                        ),
                        class_name="flex-grow",
                    ),
                    rx.el.button(
                        "Export",
                        on_click=AppState.export_data,
                        class_name="px-4 py-2 text-sm font-medium text-white bg-emerald-600 rounded-md shadow-sm hover:bg-emerald-700",
                    ),
                    class_name="flex items-center justify-between p-4 bg-gray-50 rounded-lg",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Import Data", class_name="font-medium"),
                        rx.el.p(
                            "Upload a JSON backup file to restore your data.",
                            class_name="text-sm text-gray-500",
                        ),
                        class_name="flex-grow",
                    ),
                    rx.upload.root(
                        rx.el.button(
                            "Import",
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
                            "Clear All Data", class_name="font-medium text-red-600"
                        ),
                        rx.el.p(
                            "Permanently delete all accounts and transactions.",
                            class_name="text-sm text-gray-500",
                        ),
                        class_name="flex-grow",
                    ),
                    rx.radix.primitives.dialog.root(
                        rx.radix.primitives.dialog.trigger(
                            rx.el.button(
                                "Clear Data",
                                class_name="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md shadow-sm hover:bg-red-700",
                            )
                        ),
                        rx.radix.primitives.dialog.portal(
                            rx.radix.primitives.dialog.overlay(
                                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-[51]"
                            ),
                            rx.radix.primitives.dialog.content(
                                rx.radix.primitives.dialog.title(
                                    "Confirm Deletion",
                                    class_name="text-lg font-semibold text-gray-800",
                                ),
                                rx.radix.primitives.dialog.description(
                                    "Are you sure you want to permanently delete all data? This action cannot be undone.",
                                    class_name="text-sm text-gray-600 mt-2",
                                ),
                                rx.el.div(
                                    rx.radix.primitives.dialog.close(
                                        rx.el.button(
                                            "Cancel",
                                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md shadow-sm hover:bg-gray-200",
                                        )
                                    ),
                                    rx.radix.primitives.dialog.close(
                                        rx.el.button(
                                            "Clear Data",
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