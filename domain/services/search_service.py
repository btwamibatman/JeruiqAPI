from typing import List
from domain.models.place import Place
from domain.models.search_filter import SearchFilter

def filter_places(places: List[Place], search_filter: SearchFilter) -> List[Place]:
    """Filter places according to the given SearchFilter."""
    filtered = []
    for place in places:
        if search_filter.rating_min is not None:
            if place.rating is None or place.rating < search_filter.rating_min:
                continue
        if search_filter.price_level is not None:
            if getattr(place, 'price_level', None) is None or getattr(place, 'price_level', None) > search_filter.price_level:
                continue
        if search_filter.open_now is not None:
            if getattr(place, 'open_now', None) != search_filter.open_now:
                continue
        filtered.append(place)
    return filtered