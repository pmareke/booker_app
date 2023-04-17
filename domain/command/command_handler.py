from abc import ABC, abstractmethod

from domain.command.command import Command
from domain.command.command_response import CommandResponse


class CommandHandler(ABC):
    @abstractmethod
    def process(self, command: Command) -> CommandResponse:
        raise NotImplementedError
