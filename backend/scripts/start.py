import asyncio
import os
import time

import uvicorn

from scripts.migrate import upgrade
from scripts.seed_default_interest_types import main as seed_default_interest_types

MAX_STARTUP_ATTEMPTS = 30
STARTUP_RETRY_SECONDS = 2


def run_with_retry(name: str, action) -> None:
    for attempt in range(1, MAX_STARTUP_ATTEMPTS + 1):
        try:
            action()
            return
        except Exception as exc:
            if attempt == MAX_STARTUP_ATTEMPTS:
                raise
            print(
                f"{name} failed "
                f"(attempt={attempt}/{MAX_STARTUP_ATTEMPTS}): {exc}",
                flush=True,
            )
            time.sleep(STARTUP_RETRY_SECONDS)


def run_migrations() -> None:
    upgrade("head")


def run_seed() -> None:
    asyncio.run(seed_default_interest_types())


def main() -> None:
    run_with_retry("database migration", run_migrations)
    run_with_retry("default interest type seed", run_seed)

    uvicorn.run(
        "app.main:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", "8000")),
    )


if __name__ == "__main__":
    main()
