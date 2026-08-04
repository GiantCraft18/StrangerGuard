from typing import Set
from .models import CheckResult


def is_stranger(
    user_id: int,
    contacts: Set[int],
    dialogs: Set[int],
    whitelist: Set[int],
) -> CheckResult:
    in_contacts = user_id in contacts
    in_dialogs = user_id in dialogs
    in_whitelist = user_id in whitelist

    if in_whitelist:
        return CheckResult(
            is_stranger=False,
            user_id=user_id,
            reason="В белом списке",
            in_contacts=in_contacts,
            in_dialogs=in_dialogs,
            in_whitelist=True,
        )

    if in_contacts or in_dialogs:
        return CheckResult(
            is_stranger=False,
            user_id=user_id,
            reason="Есть в контактах или диалогах",
            in_contacts=in_contacts,
            in_dialogs=in_dialogs,
            in_whitelist=False,
        )

    return CheckResult(
        is_stranger=True,
        user_id=user_id,
        reason="Незнакомец",
        in_contacts=False,
        in_dialogs=False,
        in_whitelist=False,
    )