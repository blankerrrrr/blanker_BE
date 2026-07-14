from types import SimpleNamespace

import pytest

from app.db.repositories.public_id import save_with_public_id


class FakeSession:
    def __init__(self) -> None:
        self.flush_count = 0
        self.added: object | None = None
        self.first_flush_public_id: str | None = None

    def add(self, instance: object) -> None:
        self.added = instance

    async def flush(self) -> None:
        self.flush_count += 1
        if self.added is not None and self.flush_count == 1:
            self.first_flush_public_id = self.added.user_id
            self.added.id = 7

    async def refresh(self, instance: object) -> None:
        self.refreshed = instance


@pytest.mark.asyncio
async def test_save_with_public_id_uses_final_id_after_insert() -> None:
    session = FakeSession()
    user = SimpleNamespace(id=None, user_id=None)

    saved_user = await save_with_public_id(session, user, "user_id", "user")

    assert saved_user.user_id == "user_7"
    assert session.flush_count == 2


@pytest.mark.asyncio
async def test_save_with_public_id_keeps_insert_value_non_null_before_flush() -> None:
    session = FakeSession()
    user = SimpleNamespace(id=None, user_id=None)

    await save_with_public_id(session, user, "user_id", "user")

    assert session.added is user
    assert session.first_flush_public_id is not None
    assert session.first_flush_public_id.startswith("user_pending_")
    assert user.user_id == "user_7"
