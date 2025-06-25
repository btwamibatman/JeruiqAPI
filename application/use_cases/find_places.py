from domain.services.ai_service.gemini_query_service import GeminiQueryService
from domain.services.search_service import filter_places
from domain.models.place import Place
from domain.models.search_filter import SearchFilter
from domain.exceptions import InvalidQueryException, ExternalServiceException, PlaceNotFoundException, DomainException

def find_places(user_text, gemini_service: GeminiQueryService, photon_client):
    try:
        # 1. Parse user query with AI
        user_query = gemini_service.parse_user_query(user_text)
        if not user_query or not user_query.category:
             # Raise a domain exception if AI parsing fails to yield a usable query
             raise InvalidQueryException("Could not understand the query. Please try rephrasing.")

    except Exception as e:
        # Catch potential errors from Gemini service and wrap them
        raise ExternalServiceException("Error parsing query with AI service.", original_error=e) from e

    try:
        # 2. Search Photon for places
        # Use the category from the parsed query, fallback to raw text
        search_term = user_query.category or user_text
        photon_results = photon_client.search(search_term)

        if not photon_results or not photon_results.get("features"):
             # Raise if Photon returns no results
             raise PlaceNotFoundException(f"No places found for '{search_term}'.")

    except Exception as e:
        # Catch potential errors from Photon client and wrap them
        raise ExternalServiceException("Error searching for places.", original_error=e) from e


    # 3. Convert Photon results to Place models (already done)
    places = []
    for feature in photon_results.get("features", []):
        props = feature["properties"]
        places.append(Place(
            name=props.get("name"),
            lat=feature["geometry"]["coordinates"][1],
            lon=feature["geometry"]["coordinates"][0],
            category=props.get("osm_value"),
            address=props.get("city"),
            rating=props.get("rating"),  # if available
        ))

    # 4. Filter places using domain logic (already done)
    # Ensure filters are correctly parsed from user_query.filters into SearchFilter
    try:
        # Simple conversion, might need more complex logic depending on AI output
        filter_data = {}
        if user_query.filters:
             # Example: Convert {"rating_min": 4.5} from AI to SearchFilter(rating_min=4.5)
             if 'rating_min' in user_query.filters:
                  try:
                       filter_data['rating_min'] = float(user_query.filters['rating_min'])
                  except (ValueError, TypeError):
                       print(f"Warning: Could not convert rating_min filter value {user_query.filters['rating_min']} to float.")
                       # Optionally raise InvalidQueryException here if filter is critical

        search_filter = SearchFilter(**filter_data)
        filtered_places = filter_places(places, search_filter)

    except Exception as e:
         # Catch potential errors during filtering
         raise DomainException("Error applying search filters.") from e


    return filtered_places