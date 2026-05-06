"""Main entry point for the Fincept Terminal application.

This module initializes and launches the terminal-based financial
information dashboard using Textual TUI framework.
"""

import sys
import argparse
from pathlib import Path

# Ensure the package root is importable when run directly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fincept_terminal import __version__, __app_name__


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the terminal application.

    Returns:
        argparse.Namespace: Parsed arguments object.
    """
    parser = argparse.ArgumentParser(
        prog="fincept",
        description=f"{__app_name__} — A powerful financial data terminal.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fincept                  Launch the interactive terminal
  fincept --version        Display the current version
  fincept --debug          Launch with debug logging enabled
        """,
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"{__app_name__} v{__version__}",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Enable debug mode with verbose logging.",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        default=False,
        help="Disable colored output (useful for plain terminals).",
    )
    return parser.parse_args()


def setup_logging(debug: bool = False) -> None:
    """Configure application-level logging.

    Args:
        debug (bool): If True, sets log level to DEBUG; otherwise INFO.
    """
    import logging

    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def main() -> None:
    """Primary entry point — parses arguments and launches the TUI app."""
    args = parse_args()
    setup_logging(debug=args.debug)

    import logging
    logger = logging.getLogger(__name__)
    logger.info("Starting %s v%s", __app_name__, __version__)

    try:
        # Lazy import so startup errors surface cleanly
        from fincept_terminal.app import FinceptApp

        app = FinceptApp(debug=args.debug, no_color=args.no_color)
        app.run()
    except ImportError as exc:
        print(
            f"[ERROR] Failed to import application components: {exc}\n"
            "Please ensure all dependencies are installed:\n"
            "  pip install fincept-terminal",
            file=sys.stderr,
        )
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nSession terminated by user. Goodbye!")
        sys.exit(0)
    except Exception as exc:  # noqa: BLE001
        import logging
        logging.getLogger(__name__).exception("Unhandled exception during runtime.")
        print(f"[FATAL] {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
