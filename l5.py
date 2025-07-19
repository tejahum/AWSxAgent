# complex_functions.py

import heapq
import functools
import json
import re
from typing import Any, Dict, List, Tuple


def dijkstra_shortest_paths(
    graph: Dict[Any, List[Tuple[Any, float]]], start: Any
) -> Dict[Any, float]:
    """
    Compute shortest path distances from `start` to every node in a weighted graph.
    Uses a min-heap for efficiency (O(E log V)).
    `graph` is a dict mapping node -> list of (neighbor, weight).
    Returns a dict node -> distance.
    """
    dist = {node: float("inf") for node in graph}
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist


def lru_cache(maxsize: int = 128):
    """
    Decorator to provide an LRU cache for any function.
    Evicts least-recently-used entries when cache exceeds `maxsize`.
    """
    def decorator(fn):
        cache = {}
        order = []

        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in cache:
                order.remove(key)
                order.append(key)
                return cache[key]
            result = fn(*args, **kwargs)
            cache[key] = result
            order.append(key)
            if len(order) > maxsize:
                old_key = order.pop(0)
                del cache[old_key]
            return result

        wrapped.cache_clear = lambda: (cache.clear(), order.clear())
        return wrapped
    return decorator


def parse_and_flatten_json(data: str) -> Dict[str, Any]:
    """
    Parses a nested JSON string, flattens all nested dicts into a single-level dict
    with dot-separated keys, and returns the resulting dict.
    """
    def _flatten(obj, prefix=""):
        items = {}
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_prefix = f"{prefix}{k}." if prefix else f"{k}."
                items.update(_flatten(v, new_prefix))
        elif isinstance(obj, list):
            for idx, v in enumerate(obj):
                new_prefix = f"{prefix}{idx}."
                items.update(_flatten(v, new_prefix))
        else:
            items[prefix[:-1]] = obj
        return items

    parsed = json.loads(data)
    return _flatten(parsed)


def validate_email_address(email: str) -> bool:
    """
    Uses a complex regex to validate email addresses per RFC 5322 (simplified).
    Returns True if valid, False otherwise.
    """
    pattern = (
        r"(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+"
        r"(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*|"
        r"\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21"
        r"\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b"
        r"\x0c\x0e-\x7f])*\")@"
        r"(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*"
        r"[a-zA-Z0-9])?\.)+[a-zA-Z0-9]"
        r"(?:[a-zA-Z0-9-]*[a-zA-Z0-9])?|\["
        r"(?:(?:25[0-5]\.|2[0-4][0-9]\.|[01]?[0-9]{1,2}\.){3}"
        r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]{1,2})\])"
    )
    return re.fullmatch(pattern, email) is not None


def traverse_tree(node: Dict[str, Any], visit_fn) -> None:
    """
    Recursively traverse a nested tree represented as dicts with 'children' lists.
    Calls `visit_fn(node)` for each node.
    """
    visit_fn(node)
    for child in node.get("children", []):
        traverse_tree(child, visit_fn)
