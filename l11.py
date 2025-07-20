import math
from typing import Dict, Any
from pymongo import MongoClient, errors
def control_tv(state: Dict[str, Any], button: str, value: Any = None) -> Dict[str, Any]:
    """
    Simulates pressing a button on a smart TV.

    Parameters:
    - state: dict with keys 'power' (bool), 'channel' (int), 'volume' (int)
    - button: one of 'power', 'channel_up', 'channel_down', 'set_channel', 'volume_up', 'volume_down'
    - value: required if button=='set_channel' (int channel number)

    Returns the new state dict.
    """
    new_state = state.copy()
    if button == "power":
        new_state["power"] = not new_state.get("power", False)
    elif not new_state.get("power", False):
        return new_state
    elif button == "channel_up":
        new_state["channel"] = new_state.get("channel", 1) + 1
    elif button == "channel_down":
        new_state["channel"] = max(1, new_state.get("channel", 1) - 1)
    elif button == "set_channel":
        if not isinstance(value, int) or value < 1:
            raise ValueError("Invalid channel")
        new_state["channel"] = value
    elif button == "volume_up":
        new_state["volume"] = min(100, new_state.get("volume", 10) + 1)
    elif button == "volume_down":
        new_state["volume"] = max(0, new_state.get("volume", 10) - 1)
    else:
        raise ValueError(f"Unknown button: {button}")
    return new_state