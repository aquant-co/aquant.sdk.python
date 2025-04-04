# Aquant SDK Python

**Aquant SDK Python** is a comprehensive Software Development Kit designed to streamline interactions with market data and trade services. Built with Python 3.13, it leverages modern features and optimizations to provide a robust and efficient development experience. The SDK utilizes [Poetry](https://python-poetry.org/) for dependency management and packaging, ensuring a consistent and reliable environment. Additionally, it supports development within [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers), facilitating a seamless and reproducible development setup.

## Table of Contents

- [Aquant SDK Python](#aquant-sdk-python)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Initializing the SDK](#initializing-the-sdk)
    - [Retrieving the Current Order Book](#retrieving-the-current-order-book)
    - [Fetching Trades](#fetching-trades)
    - [Obtaining Broker Information](#obtaining-broker-information)
    - [Accessing Securities Details](#accessing-securities-details)
    - [OHLCV Calculations](#ohlcv-calculations)
  - [Development Environment](#development-environment)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- **Asynchronous Operations**: Leverages Python's `asyncio` for non-blocking interactions with services.
- **Dependency Injection**: Utilizes automatic dependency injection for managing service components.
- **Market Data Access**: Provides methods to interact with market data services.
- **Trade Services**: Facilitates operations related to trade functionalities.
- **OHLCV Calculations**: Offers auxiliary functions for Open, High, Low, Close, Volume calculations on trade data.

## Installation

Ensure you have Python 3.13 installed. You can download it from the [official Python website](https://www.python.org/downloads/release/python-3130/). citeturn0search0

Install [Poetry](https://python-poetry.org/docs/) for dependency management:

```bash
pip install poetry
```

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/aquant-sdk-python.git
cd aquant-sdk-python
poetry install
```

## Usage

### Initializing the SDK
To begin using the SDK, you are going to need create a `.env` file in the root of your project, like this:

```bash
AQUANT_NATS_USER=your-nats-user
AQUANT_NATS_PASSWORD=your-nats-password
REDIS_URL=redis-uri
NATS_URL=nats-broker-uri
```


Then you can initialize the `Aquant` class with the necessary configuration:

```python
from aquant import Aquant
from aquant.core.config import settings # This is an example of how you can you your .env variables

aquant = await Aquant.create(
    redis_url=settings.REDIS_URL,
    nats_servers=[settings.NATS_URL],
    nats_user=settings.AQUANT_NATS_USER,
    nats_password=settings.AQUANT_NATS_PASSWORD,
    redis_use_tls=False # or True if you use TLS or rediss:// protocol
)
```

### Retrieving the Current Order Book

Fetch the current order book for specific tickers:

```python
order_book_df = aquant.get_current_order_book(["AAPL", "MSFT"])
print(order_book_df)
```

### Fetching Trades

Retrieve trades within a specified time range:

```python
from datetime import datetime

ticker = "AAPL"
start_time = datetime(2023, 1, 1)
end_time = datetime(2023, 1, 31)

trades_df = await aquant.get_trades(ticker=ticker, start_time=start_time, end_time=end_time)
print(trades_df)
```

### Obtaining Broker Information

Get broker details using a foreign key ID:

```python
fk_id = 1234
broker_info = await aquant.get_broker(fk_id=fk_id)
print(broker_info)
```

### Accessing Securities Details

Fetch security information based on ticker, asset, or expiration date:

```python
from datetime import datetime

ticker = "VALE3"
asset = "VALE"
expires_at = datetime(2025, 12, 31)

security_info = await aquant.get_securities(ticker=ticker, asset=asset, expires_at=expires_at)
print(security_info)
```

### OHLCV Calculations

Perform OHLCV calculations on trade data:

```python
ohlcv_data = aquant.calculate_ohlcv(trades_df)
print(ohlcv_data)
```

## Development Environment

For a consistent development environment, the project supports [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) in Visual Studio Code. This allows you to develop inside a Docker container, ensuring all dependencies and tools are available and consistent across different setups.

To set up the Dev Container:

1. Install [Docker](https://www.docker.com/get-started) and [Visual Studio Code](https://code.visualstudio.com/).
2. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) for Visual Studio Code.
3. Open the project in Visual Studio Code.
4. When prompted, reopen the project in the Dev Container.

For more information on Dev Containers, refer to the [official documentation](https://code.visualstudio.com/docs/devcontainers/containers).

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

*Note: This README provides an overview of the Aquant SDK Python project, its features, and usage. For detailed documentation and advanced configurations, please refer to the project's official documentation.* 