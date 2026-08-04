from typing import Callable, Set, Optional
from .models import Config, CheckResult, ActionResult, ActionType
from .detectors import is_stranger
from .actions import perform_block, perform_ban
from .cache import Cache
from .exceptions import NotStrangerError, ConfigError


class StrangerGuard:
    def __init__(
        self,
        get_contacts: Callable[[], Set[int]],
        get_dialogs: Callable[[], Set[int]],
        block_func: Optional[Callable[[int], bool]] = None,
        ban_func: Optional[Callable[[int, int], bool]] = None,
        config: Optional[Config] = None,
        whitelist: Optional[Set[int]] = None,
    ):
        self.get_contacts = get_contacts
        self.get_dialogs = get_dialogs
        self.block_func = block_func
        self.ban_func = ban_func
        self.config = config or Config()
        self.whitelist = whitelist or set()
        self.cache = Cache(ttl=self.config.cache_ttl)

    def check(self, user_id: int) -> CheckResult:
        cache_key = f"check_{user_id}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        result = is_stranger(
            user_id=user_id,
            contacts=self.get_contacts(),
            dialogs=self.get_dialogs(),
            whitelist=self.whitelist,
        )
        self.cache.set(cache_key, result)
        return result

    def is_stranger(self, user_id: int) -> bool:
        return self.check(user_id).is_stranger

    def block(self, user_id: int, force: bool = False) -> ActionResult:
        if not self.block_func:
            raise ConfigError("block_func не передан")

        if not force:
            result = self.check(user_id)
            if not result.is_stranger:
                raise NotStrangerError(result.reason)

        return perform_block(user_id, self.block_func)

    def ban(self, user_id: int, chat_id: int, force: bool = False) -> ActionResult:
        if not self.ban_func:
            raise ConfigError("ban_func не передан")

        if not force:
            result = self.check(user_id)
            if not result.is_stranger:
                raise NotStrangerError(result.reason)

        return perform_ban(user_id, chat_id, self.ban_func)

    def add_to_whitelist(self, user_id: int) -> None:
        self.whitelist.add(user_id)
        self.cache.delete(f"check_{user_id}")

    def remove_from_whitelist(self, user_id: int) -> None:
        self.whitelist.discard(user_id)
        self.cache.delete(f"check_{user_id}")

    def clear_cache(self) -> None:
        self.cache.clear()