"""Library allowing using tuyau like pipe."""

from collections.abc import Callable
from typing import Any


class Tube:
    """A tuyau that processes values through a sequence of steps."""

    _steps: tuple[Callable[[Any], Any], ...]

    def __init__(self, *args: Callable[[Any], Any]) -> None:  # noqa: ANN101
        """Initialize the Tuyau with a sequence of steps.

        Args:
            *args (tuple[Callable[[Any], Any]]): callable steps.
        """
        self._steps = args

    def __call__(self, value: Any) -> Any:  # noqa: ANN101, ANN401
        """Process a value through the tuyau.

        Args:
            value (Any): The input value to be processed.

        Return:
            Any: The output value after processing through all the steps.
        """
        _val = value
        for step in self._steps:
            _val = step(_val)
        return _val

    def send(self, value: Any) -> Any:  # noqa: ANN101, ANN401
        """Process a value through the tuyau. alias of call.

        Args:
            value (Any): The input value to be processed.

        Return:
            Any: The output value after processing through all the steps.
        """
        return self(value)
