import sys


def main() -> int:
    """Compile the Reflex app in dry-run mode to catch compile-time errors.

    Returns a non-zero exit code if compilation fails.
    """
    try:
        # Import inside function to avoid side effects when this module is inspected.
        from app.app import app  # type: ignore

        # Trigger the Reflex compiler without starting the server.
        # This exercises page/component compilation (the same code path that fails at runtime).
        app._compile(dry_run=True)  # pyright: ignore[reportPrivateUsage]
        print("Reflex compile check: OK")
        return 0
    except Exception as exc:  # noqa: BLE001 - we want to report any failure
        print("Reflex compile check: FAILED")
        print(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())



