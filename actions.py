from typing import Callable, Optional
from .models import ActionResult, ActionType
from .exceptions import ActionFailedError


def perform_block(user_id: int, block_func: Callable[[int], bool]) -> ActionResult:
    try:
        ok = block_func(user_id)
        return ActionResult(
            success=ok,
            action=ActionType.BLOCK,
            user_id=user_id,
            message="Пользователь заблокирован" if ok else "Не удалось заблокировать",
        )
    except Exception as e:
        return ActionResult(
            success=False,
            action=ActionType.BLOCK,
            user_id=user_id,
            message=str(e),
            error=e,
        )


def perform_ban(
    user_id: int,
    chat_id: int,
    ban_func: Callable[[int, int], bool],
) -> ActionResult:
    try:
        ok = ban_func(user_id, chat_id)
        return ActionResult(
            success=ok,
            action=ActionType.BAN,
            user_id=user_id,
            message="Пользователь забанен" if ok else "Не удалось забанить",
        )
    except Exception as e:
        return ActionResult(
            success=False,
            action=ActionType.BAN,
            user_id=user_id,
            message=str(e),
            error=e,
        )