import abc
import numbers
import typing

from . import schedulers


class Optimizer(abc.ABC):
    """Optimizer interface.

    Every optimizer inherits from this base interface.

    Parameters
    ----------
    lr

    Attributes
    ----------
    learning_rate : float
        Returns the current learning rate value.

    """

    def __init__(self, lr: typing.Union[schedulers.Scheduler, float]):
        if isinstance(lr, numbers.Number):
            lr = schedulers.Constant(lr)
        self.lr = lr
        self.n_iterations = 0

    @property
    def learning_rate(self) -> float:
        return self.lr.get(self.n_iterations)

    def update_before_pred(self, w: dict) -> dict:
        """Updates a weight vector before a prediction is made.

        Parameters:
            w (dict): A dictionary of weight parameters. The weights are modified in-place.

        Returns:
            The updated weights.

        """
        return w

    @abc.abstractmethod
    def _update_after_pred(self, w: dict, g: dict) -> dict:
        """Updates a weight vector given a gradient."""
        raise NotImplementedError

    def update_after_pred(self, w: dict, g: dict) -> dict:
        """Updates a weight vector given a gradient.

        Parameters:
            w (dict): A dictionary of weight parameters. The weights are modified in-place.
            g (dict): A dictionary of gradients.

        Returns:
            The updated weights.

        """

        # Update the weights
        w = self._update_after_pred(w, g)

        # Update the iteration counter
        self.n_iterations += 1

        return w

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return f'{self.__class__.__name__}({vars(self)})'
