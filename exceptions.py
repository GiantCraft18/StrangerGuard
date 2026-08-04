class StrangerGuardError(Exception):
    """Базовое исключение библиотеки"""
    pass


class NotStrangerError(StrangerGuardError):
    """Пользователь не является незнакомцем"""
    pass


class ActionFailedError(StrangerGuardError):
    """Не удалось выполнить действие"""
    pass


class ConfigError(StrangerGuardError):
    """Ошибка конфигурации"""
    pass