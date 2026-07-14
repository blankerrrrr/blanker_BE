import argparse
from pathlib import Path

from alembic.config import Config

from alembic import command

BACKEND_DIR = Path(__file__).resolve().parents[1]
ALEMBIC_INI = BACKEND_DIR / "alembic.ini"


def alembic_config() -> Config:
    return Config(ALEMBIC_INI)


def upgrade(revision: str) -> None:
    command.upgrade(alembic_config(), revision)


def downgrade(revision: str) -> None:
    command.downgrade(alembic_config(), revision)


def current() -> None:
    command.current(alembic_config())


def history() -> None:
    command.history(alembic_config())


def revision(message: str, autogenerate: bool) -> None:
    command.revision(
        alembic_config(),
        message=message,
        autogenerate=autogenerate,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Alembic migration helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    upgrade_parser = subparsers.add_parser("upgrade")
    upgrade_parser.add_argument("revision", nargs="?", default="head")

    downgrade_parser = subparsers.add_parser("downgrade")
    downgrade_parser.add_argument("revision")

    subparsers.add_parser("current")
    subparsers.add_parser("history")

    revision_parser = subparsers.add_parser("revision")
    revision_parser.add_argument("-m", "--message", required=True)
    revision_parser.add_argument("--autogenerate", action="store_true")

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    match args.command:
        case "upgrade":
            upgrade(args.revision)
        case "downgrade":
            downgrade(args.revision)
        case "current":
            current()
        case "history":
            history()
        case "revision":
            revision(args.message, args.autogenerate)


if __name__ == "__main__":
    main()
