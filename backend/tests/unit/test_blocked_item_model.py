from app.db.models.blocked_item import BlockedItem


def test_interest_target_fk_sets_blocked_item_target_to_null_on_delete() -> None:
    foreign_key = next(
        foreign_key
        for foreign_key in BlockedItem.__table__.c.interest_target_id.foreign_keys
    )

    assert foreign_key.target_fullname == "interest_targets.interest_target_id"
    assert foreign_key.ondelete == "SET NULL"
