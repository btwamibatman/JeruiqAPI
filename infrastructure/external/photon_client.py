import requests
import logging # Import logging
from typing import Optional, Dict, Any

# Configure logging (can be done in app.py or a separate logging config)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PhotonClient:
    def __init__(self, base_url: str = "https://photon.komoot.io/api/"):
        self.base_url = base_url
        logger.info(f"Initialized PhotonClient with base URL: {self.base_url}")

    def search(self, query: str, bbox: str = None, limit: int = 20, lang: str = "en") -> Dict[str, Any]:
        """
        Search for places using the Photon API.
        :param query: Search query string.
        :param bbox: Optional bounding box.
        :param limit: Number of results to return.
        :param lang: Language code.
        :return: JSON response as dict.
        :raises ExternalServiceException: If the API call fails.
        """
        params = {
            "q": query,
            "lang": lang,
            "limit": limit
        }
        if bbox:
            params["bbox"] = bbox

        url = f"{self.base_url}?" # Construct the full URL for logging
        logger.info(f"Calling Photon API: GET {url} with params {params}")

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            logger.info(f"Photon API call successful. Status: {response.status_code}")
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any request-related errors (connection, timeout, HTTP errors)
            logger.error(f"Error calling Photon API: {e}", exc_info=True) # Log the error details
            # Raise a domain-specific exception
            from domain.exceptions import ExternalServiceException # Import here to avoid circular dependency if domain imports infra
            raise ExternalServiceException(f"Failed to search for places using Photon: {e}") from e
        except Exception as e:
             # Catch any other unexpected errors
             logger.error(f"An unexpected error occurred during Photon API call: {e}", exc_info=True)
             from domain.exceptions import ExternalServiceException
             raise ExternalServiceException(f"An unexpected error occurred during Photon search: {e}") from e
