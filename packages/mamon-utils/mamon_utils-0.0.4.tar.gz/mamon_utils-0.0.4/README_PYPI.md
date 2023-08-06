# Mamon Utilities
A set of tools and utilities for Python Development


## Installation
```sh
pip install mamon-utils
```

## Usage
To use any of these modules, just import from `mamonutils`.

### Database
This module makes it easy to connect to our PostgreSQL databases. To use it, you have to add a `.env` file in the root of your project specifying the following environment variables:
```.env
DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
```

#### Example Usage
```python
from mamonutils import Database, dotenv

# Load environment variables
dotenv()

# Connect to clients database
db = Database('clients')
cursor = db.cursor

cursor.execute('SELECT * from clients')
result = cursor.fetchall()
print(result)

# Disconnect
db.disconnect()
```

### get_dimensions
A utility that allows you to retrieve the dimensions (width and height) of an image from a given URL. The utility uses the requests module to fetch the image data and the PIL (Python Imaging Library) module to extract the image metadata. The utility is designed to be flexible, allowing users to handle exceptions and errors according to their specific needs.

#### Example Usage
The utility takes a URL string as input and returns a dictionary containing the image's width and height.
```python
from mamonutils import get_dimensions

try:
    image_url = "https://example.com/image.jpg"
    dimensions = get_dimensions(image_url)
    print("Image Dimensions:")
    print(f"Width: {dimensions['width']}")
    print(f"Height: {dimensions['height']}")
except ValueError as e:
    print(f"Error: {str(e)}")
```