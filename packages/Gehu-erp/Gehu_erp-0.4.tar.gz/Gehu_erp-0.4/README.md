# Gehu_erp - A Python Library for Interacting with GEHU Student API

Gehu_erp is a Python library that provides a simple interface for interacting with the GEHU (Generic Educational Institution) Student API. With this library, you can perform various actions, such as logging in, retrieving student details, and more.

## Installation

You can install Gehu_erp using pip:

```
pip install Gehu_erp
```

## Usage

```python
import erp

# Create a client instance
client = erp.Client()

# Generate session and login
user = "your_username"
password = "your_password"
client.login(user, password)

# Get student details
data = client.info()

# Print student details
for key, value in data.items():
    print(f"{key}: {value}")
```

For more information and examples, please visit the GitHub repository.

## Setup and Installation

To use Gehu_erp, you need to install it via pip. First, ensure you have Python installed, then open a terminal and run the following command:

```
pip install Gehu_erp
```
## Docs

For more information and examples, please visit the [documentation](https://gehu-erp.readthedocs.io/en/latest/index.html).


## Dependencies

Gehu_erp depends on the following Python libraries:
- requests
- Pillow
- beautifulsoup4

These dependencies will be automatically installed when you install Gehu_erp.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

If you would like to contribute to Gehu_erp, feel free to submit a pull request or open an issue on the GitHub repository.

## Acknowledgments

- Thanks to the developers of `requests`, `Pillow`, and `beautifulsoup4` for their excellent libraries.
- Special thanks to the developers and maintainers of the GEHU Student API for providing the API that this library interacts with.```