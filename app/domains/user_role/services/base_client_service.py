from app.core.exceptions.http import HTTPExceptionHandler
from app.core.logger.logger import LoggerInterface
from app.domains.telegram.services.formatters import PlainTextFormatter
from app.infra.adapters.http import HTTPAdapter


class BaseClientService:
    """
    Base service for handling HTTP requests and formatting responses.
    """

    def __init__(
        self,
        http_adapter: HTTPAdapter,
        logger: LoggerInterface,
        exception_handler: HTTPExceptionHandler,
        formatter: PlainTextFormatter,
        base_url: str,
    ):
        """
        Initializes the base client service with dependencies.

        Args:
            http_adapter (HTTPAdapter): HTTP client adapter for requests.
            logger (LoggerInterface): Logger instance for structured logging.
            exception_handler (HTTPExceptionHandler): Handles HTTP exceptions gracefully.
            formatter (PlainTextFormatter): Formats response data.
            base_url (str): Base URL for the API.
        """
        self.http_adapter = http_adapter
        self.logger = logger
        self.exception_handler = exception_handler
        self.formatter = formatter
        self.base_url = base_url

    async def fetch_data(
        self, endpoint: str, params: dict = None, headers: dict = None
    ) -> dict:
        """
        Fetches raw data from the given API endpoint.

        Args:
            endpoint (str): API endpoint to query.
            params (dict): Query parameters for the request.
            headers (dict): Headers for the request.

        Returns:
            dict: The raw response data.
        """
        try:
            # Log the request details
            url = f"{self.base_url}{endpoint}"
            self.logger.info(
                f"Fetching data from URL: {url} with params: {params}, headers: {headers}"
            )

            # Perform the HTTP GET request
            response = await self.http_adapter.get(
                url=url,
                params=params or {"date": "last-working-day"},
                headers=headers or {"Accept": "text/plain"},
            )

            if not response:
                self.logger.warning(f"No response received for URL: {url}")
                return {}

            self.logger.info(f"Data fetched successfully from URL: {url}")
            return response

        except Exception as err:
            self.logger.error(f"Error fetching data from endpoint {endpoint}: {err}")
            raise

    def format_response(self, raw_data: dict, context: str) -> str:
        """
        Formats the raw response data using the formatter.

        Args:
            raw_data (dict): The raw data fetched from the API.
            context (str): Context for the operation (e.g., 'trades', 'positions').

        Returns:
            str: Formatted data or error message.
        """
        try:
            if not raw_data:
                self.logger.warning(
                    f"No data available to format for context: {context}"
                )
                return self.formatter.format_not_found(context)

            formatted_data = self.formatter.format(raw_data)
            self.logger.info(f"Data formatted successfully for context: {context}")
            return formatted_data

        except Exception as err:
            self.logger.error(f"Error formatting data for context {context}: {err}")
            return f"Failed to format data for {context}."

    async def fetch_and_format_response(
        self,
        endpoint: str,
        context: str,
        params: dict = None,
        headers: dict = None,
    ) -> str:
        """
        Fetches data from the given endpoint and formats the response.

        Args:
            endpoint (str): API endpoint to query.
            context (str): Context for logging (e.g., 'trades', 'open positions').
            params (dict): Query parameters for the request.
            headers (dict): Headers for the request.

        Returns:
            str: Formatted data or error message.
        """
        try:
            # Fetch raw data
            response = await self.fetch_data(endpoint, params, headers)

            content_type = response.headers.get("Content-Type", "").lower()

            if "application/json" in content_type:
                raw_data = response.json()
            elif "text/plain" in content_type:
                raw_data = {"data": response.text}
            else:
                raw_data = {"data": response.content}

            # Format the fetched data
            formatted_data = self.format_response(raw_data, context)

            return formatted_data

        except Exception as err:
            self.logger.error(
                f"Failed to fetch and format data for context {context}: {err}"
            )
            return self.exception_handler.handle_exception(err)
