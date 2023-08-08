"""Generates tuning parameters for isel ramp current and cap select.

Uses linear regression by finding the slope of the average channel data
between the highest and lowest value of cap select at different ramp current
values. The slope and y-int is then used to determine what values of ramp
current and cap select will get the channel average to the target value.

The tool will return a dict with the register names as the keys and the values
is a list of values to program per channel.

    Tuning parameters are of the form:
    {
        0 (Channel): {
            isel_ramp_current: (value),
            isel_cap_select: (value),
        }
    }
"""
from .upac96 import Upac96ConversionRampOptimizer


def get_conversion_ramp_optimizer(board):
    """Sets the appropriate isel ramp/cap to put the channels in midrange.

    Args:
        board (Board): the board
        channels (list[int]): channels to generate pedestals for. Defaults to all channels.

    Returns:
        An instantiated Conversion ramp optimizer for the given board.

    Raises:
        NotImplementedError if the given board does not support pedestals.
    """

    conversion_ramp_optimizers = {
        "upac96": Upac96ConversionRampOptimizer,
    }.get(board.model, None)

    if not conversion_ramp_optimizers or not board.is_feature_enabled(
        "conversion_ramp_optimizer"
    ):
        raise NotImplemented(
            f'Board "{board.model}" does not have support for the conversion ramp optimizer.'
        )
    return conversion_ramp_optimizers(board)
