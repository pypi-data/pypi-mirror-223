from dataclasses import dataclass
from typing import Any

from pybotterfly.bot.returns.message import Return
from pybotterfly.base_config import BaseConfig
from pybotterfly.bot.throttlers import ThrottledResource
from pybotterfly.bot.logger import BaseLogger, Log, DefaultLogger


@dataclass()
class _Messenger:
    """
    Represents a messaging platform that the bot can respond to.

    :param trigger: The messaging platform that triggers the reply.
    :type trigger: BaseConfig.ADDED_MESSENGERS
    :param reply_func: The function that sends the response.
    :type reply_func: Any
    :param messages_per_second: The maximum number of messages the bot can
        send per second.
    :type messages_per_second: int
    :param _throttler: A ThrottledResource object that throttles the rate at
        which messages can be sent. Defaults to None.
    :type _throttler: ThrottledResource or None
    """

    trigger: BaseConfig.ADDED_MESSENGERS
    reply_func: Any
    messages_per_second: int
    _throttler: ThrottledResource | None = None


@dataclass()
class MessengersDivision:
    """
    A class that represents a division of messengers to answer. Contains a
    list of _Messenger objects that correspond to specific messaging
    platforms, and a boolean attribute that indicates whether the list
    has been compiled or not.

    :param config: An instance of the BaseConfig class that represents the
        base configuration options for the bot.
    :type config: BaseConfig

    :param logger: An instance of the BaseLogger class that represents the
        base logger for the bot.
    :type logger: BaseLogger

    :param _messengers_to_answer: The list of _Messenger objects that
        correspond to specific messaging platforms.
    :type _messengers_to_answer: List[_Messenger]

    :param _compiled: A boolean indicating whether the list of
        _Messenger objects has been compiled or not.
    :type _compiled: bool
    """

    def __init__(
        self,
        config: BaseConfig = BaseConfig,
        logger: BaseLogger | None = None,
    ) -> None:
        self.config = config
        self._logger = (
            logger if logger != None else DefaultLogger(config=config)
        )
        self._messengers_to_answer = []
        self._compiled = False

    def register_messenger(
        self,
        trigger: BaseConfig.ADDED_MESSENGERS,
        reply_func: Any,
        messages_per_second: int,
    ) -> None:
        """
        Registers a new messenger to reply with, along with its trigger, reply
        function, and messages per second limit. The messenger is added to the
        `_messengers_to_answer` list.

        Raises a `ValueError` if the `Bot` object has already been compiled, or
        if the new messenger to reply has the same `trigger` as an existing one
        or the same `reply_func` as an existing one.

        :param trigger: The messenger trigger to register.
        :type trigger: BaseConfig.ADDED_MESSENGERS

        :param reply_func: The reply function to associate with the messenger.
        :type reply_func: Any

        :param messages_per_second: The limit of messages that can be sent per
            second by the messenger.
        :type messages_per_second: int
        """

        if self._compiled:
            error_str = (
                f"Messengers already compiled"
                f"\nEnsure to add messengers before compiling"
            )
            raise ValueError(error_str)
        if messages_per_second <= 0:
            error_str = f"Can't use negative values"
            raise ValueError(error_str)
        new_messenger_to_reply = _Messenger(
            trigger=trigger,
            reply_func=reply_func,
            messages_per_second=messages_per_second,
        )
        if new_messenger_to_reply in self._messengers_to_answer:
            error_str = f"Messenger already registered"
            raise ValueError(error_str)
        if reply_func in [
            func.reply_func for func in self._messengers_to_answer
        ]:
            error_str = f"Same reply func already used"
            raise ValueError(error_str)
        self._messengers_to_answer.append(new_messenger_to_reply)

    def compile(self) -> None:
        """
        Compiles the registered messengers by initializing a `ThrottledResource`
        for each messenger with the given messages per second rate and reply
        function. This method must be called after all messengers have been
        registered and before starting the client.

        :return: None
        :rtype: NoneType

        :raises ValueError: If the messengers are already compiled.
        """

        if self._compiled:
            raise ValueError(f"Messengers already compiled")
        for messenger in self._messengers_to_answer:
            messenger._throttler = ThrottledResource(
                delay=1.0 / messenger.messages_per_second,
                func_to_throttle=messenger.reply_func,
            )
            self._logger.log(
                log=Log(
                    level="INFO",
                    text=(
                        f"Added throttler for Messenger '{messenger.trigger}' "
                        f"with rate of {messenger.messages_per_second} "
                        f"messages per second"
                    ),
                )
            )
        self._logger.log(
            log=Log(
                level="INFO",
                text=(f"[SUCCESS] Messengers compiled successfully\n"),
                starts_with=f"\n",
            )
        )
        if not self._compiled:
            self._compiled = True

    async def get_func(self, return_message: Return) -> None:
        """
        If the list of `_Messenger` objects has been compiled, this method
        finds the existing `_Messenger` object that corresponds to the
        specified `messenger` and makes an asynchronous query to it using
        the specified `return_message`. If no matching `_Messenger` object is
        found, an error message is printed.

        :param return_message: The return type for the query.
        :type return_message: Return
        """

        if not self._compiled:
            self._logger.log(
                log=Log(level="ERROR", text=(f"Messengers are not compiled"))
            )
            return
        for existing_messenger in self._messengers_to_answer:
            if existing_messenger.trigger == return_message.user_messenger:
                await existing_messenger._throttler.query(return_message)
                return
        self._logger.log(
            log=Log(
                level="ERROR",
                text=(
                    f"Needed messenger "
                    f"'{return_message.user_messenger}' wasn't registered"
                ),
            )
        )
