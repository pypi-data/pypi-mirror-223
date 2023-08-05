from abc import abstractmethod
from typing import Any, Dict, Optional, Protocol

from aiogram.fsm.state import State
from aiogram.types import Message

from aiogram_dialog.api.entities import (
    ChatEvent, Context, Data, ShowMode, Stack, StartMode,
)


class BaseDialogManager(Protocol):
    @abstractmethod
    async def done(self, result: Any = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def start(
            self,
            state: State,
            data: Data = None,
            mode: StartMode = StartMode.NORMAL,
            show_mode: ShowMode = ShowMode.AUTO,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def switch_to(self, state: State) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, data: Dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def bg(
            self,
            user_id: Optional[int] = None,
            chat_id: Optional[int] = None,
            stack_id: Optional[str] = None,
            load: bool = False,  # load chat and user
    ) -> "BaseDialogManager":
        raise NotImplementedError


class DialogManager(BaseDialogManager, Protocol):
    @property
    @abstractmethod
    def event(self) -> ChatEvent:
        raise NotImplementedError

    @abstractmethod
    async def mark_closed(self) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def middleware_data(self) -> Dict:
        """Middleware data."""
        raise NotImplementedError

    @property
    @abstractmethod
    def dialog_data(self) -> Dict:
        """Dialog data for current context."""
        raise NotImplementedError

    @property
    @abstractmethod
    def start_data(self) -> Dict:
        """Start data for current context."""
        raise NotImplementedError

    @property
    @abstractmethod
    def show_mode(self) -> ShowMode:
        """Get current show mode, used for next show action."""
        raise NotImplementedError

    @show_mode.setter
    @abstractmethod
    def show_mode(self, show_mode: ShowMode) -> None:
        """Set current show mode, used for next show action."""
        raise NotImplementedError

    @abstractmethod
    def is_preview(self) -> bool:
        """Check if this manager is used only to generate dialog preview."""
        raise NotImplementedError

    @abstractmethod
    async def show(self) -> Message:
        """Show current state to the user."""
        raise NotImplementedError

    @abstractmethod
    async def answer_callback(self) -> None:
        """Answer to a callback query."""
        raise NotImplementedError

    @abstractmethod
    def current_context(self) -> Context:
        """
        Get current dialog context.

        :raise NoContextError if there is no open dialog
        """
        raise NotImplementedError

    @abstractmethod
    def has_context(self) -> bool:
        """Check if there is current context."""
        raise NotImplementedError

    @abstractmethod
    def current_stack(self) -> Stack:
        """Get current dialog stack."""
        raise NotImplementedError

    @abstractmethod
    async def next(self) -> None:
        """Switch to the next state within current dialog."""
        raise NotImplementedError

    @abstractmethod
    async def back(self) -> None:
        """Switch to the previous state within current dialog."""
        raise NotImplementedError

    @abstractmethod
    def find(self, widget_id) -> Optional[Any]:
        """
        Find a widget in current dialog by its id.

        Returns managed adapdter for found widget,
        which does not require to pass manager and has only subset of methods.
        """
        raise NotImplementedError

    @abstractmethod
    async def reset_stack(self, remove_keyboard: bool = True) -> None:
        """
        Reset current stack.

        No callbacks are called, contexts are removed from storage.
        """
        raise NotImplementedError

    @abstractmethod
    async def load_data(self) -> Dict:
        """Load data for current state."""
        raise NotImplementedError

    @abstractmethod
    async def close_manager(self) -> None:
        """Release all resources and disable usage of many methods."""
        raise NotImplementedError
