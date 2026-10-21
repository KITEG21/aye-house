"""Command-line utilities.

Usage:
    uv run python -m app.cli create-superuser --email admin@example.com --username admin
    uv run python -m app.cli seed-zones
"""

import argparse
import asyncio
import getpass

from pydantic import ValidationError

from app.core.database import get_session_context
from app.core.exceptions import ConflictError
from app.features.users.repository import UserRepository
from app.features.users.schemas import UserCreate
from app.features.users.service import UserService
from app.features.zones.seeder import seed_zones


async def create_superuser(email: str, username: str, password: str, full_name: str | None) -> None:
    """Create a user and grant superuser rights (also promotes an existing email)."""
    async with get_session_context() as session:
        repository = UserRepository(session)
        user = await repository.get_by_email(email)
        if user is None:
            try:
                created = await UserService(session).create_user(
                    UserCreate(
                        email=email, username=username, password=password, full_name=full_name
                    )
                )
            except ConflictError as err:
                raise SystemExit(f"Error: {err.message} {err.details}") from err
            except ValidationError as err:
                raise SystemExit(f"Error: {err}") from err
            user = await repository.get_by_id(created.id)
            assert user is not None

        user.is_superuser = True
        user.is_active = True
        print(f"Superuser ready: {user.email} ({user.username})")  # noqa: T201


async def run_seed_zones() -> None:
    """Load the fixed provinces, municipalities and neighborhoods."""
    async with get_session_context() as session:
        result = await seed_zones(session)
    print(  # noqa: T201
        f"Zones seeded: {result.provinces} provinces, {result.municipalities} municipalities, "
        f"{result.neighborhoods} neighborhoods added"
    )


def main() -> None:
    """Parse arguments and run the requested command."""
    parser = argparse.ArgumentParser(prog="python -m app.cli")
    commands = parser.add_subparsers(dest="command", required=True)

    superuser = commands.add_parser("create-superuser", help="Create or promote a superuser")
    superuser.add_argument("--email", required=True)
    superuser.add_argument("--username", required=True)
    superuser.add_argument("--full-name", default=None)
    superuser.add_argument("--password", help="Prompted for if omitted")

    commands.add_parser("seed-zones", help="Load fixed zones (idempotent)")

    args = parser.parse_args()
    if args.command == "create-superuser":
        password = args.password or getpass.getpass("Password: ")
        asyncio.run(create_superuser(args.email, args.username, password, args.full_name))
    elif args.command == "seed-zones":
        asyncio.run(run_seed_zones())


if __name__ == "__main__":
    main()
