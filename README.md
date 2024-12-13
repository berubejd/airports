# Airports Library

A comprehensive Python library for airport data management and querying heavily influenced by [Tim Rogers' Airports gem](https://github.com/timrogers/airports). This library provides fast, efficient lookups for airport information using IATA codes, ICAO codes, cities, regions, and countries.

## Features

- Efficient lookup of airports by:
  - IATA code (e.g., "LAX")
  - ICAO code (e.g., "KLAX")
  - City name (e.g., "Los Angeles")
  - City code (e.g., "LAX")
  - Region/State (e.g., "California")
  - Region code (e.g., "US-CA")
  - Country (e.g., "United States")
  - Country code (e.g., "US")
- Fuzzy matching for city names
- Distance calculation between airports using the Haversine formula
- Lazy loading of data for optimal memory usage
- Type hints for better IDE support
- Comprehensive error handling

## Installation

```bash
pip install airports
```

## Quick Start

```python
from airports import Airports

# Initialize the library
airports = Airports()

# Look up an airport by IATA code
lax = airports.find_by_iata_code("LAX")
print(f"Found {lax['name']} in {lax['city']}, {lax['country']}")

# Find all airports in a city
nyc_airports = airports.find_all_by_city_code("NYC")
for airport in nyc_airports:
    print(f"{airport['name']} ({airport['iata']})")

# Calculate distance between airports
distance = airports.distance_between("JFK", "LAX")
print(f"Distance: {distance:.1f} km")
```

## API Reference

### Main Class: `Airports`

#### Basic Lookups

- `find_by_iata_code(iata_code: str) -> Optional[Dict]`
  - Find airport by 3-letter IATA code
  - Returns None if not found

- `find_by_icao_code(icao_code: str) -> Optional[Dict]`
  - Find airport by 4-letter ICAO code
  - Returns None if not found

#### City-based Lookups

- `find_all_by_city(city_name: str) -> List[Dict]`
  - Find all airports in a given city
  - Case-insensitive search

- `find_all_by_city_code(city_code: str) -> List[Dict]`
  - Find all airports with a specific 3-letter city code
  - Returns empty list if none found

- `fuzzy_find_city(city_name: str, cutoff: float = 0.6) -> List[Dict]`
  - Find airports in cities with names similar to input
  - Adjustable similarity threshold (cutoff)

#### Region and Country Lookups

- `find_all_by_region(region_name: str) -> List[Dict]`
  - Find all airports in a given region/state
  - Case-insensitive search

- `find_all_by_region_code(region_code: str) -> List[Dict]`
  - Find all airports by region code (e.g., "US-NY")
  - Returns empty list if none found

- `find_all_by_country(country_name: str) -> List[Dict]`
  - Find all airports in a given country
  - Case-insensitive search

- `find_all_by_country_code(country_code: str) -> List[Dict]`
  - Find all airports by 2-letter country code
  - Returns empty list if none found

#### Utility Methods

- `distance_between(airport1: Union[str, Dict], airport2: Union[str, Dict]) -> Optional[float]`
  - Calculate distance between two airports in kilometers
  - Accept either IATA codes or airport dictionaries
  - Returns None if either airport not found or missing coordinates

#### Properties

- `iata_codes: List[str]` - Get all IATA codes in dataset
- `icao_codes: List[str]` - Get all ICAO codes in dataset
- `city_codes: List[str]` - Get all city codes in dataset

### Airport Data Structure

Each airport is represented as a dictionary with the following fields:

```python
{
    # Basic Information
    "name": str,             # Full airport name
    "city": str,             # City name
    "city_code": str,        # IATA city code
    "country": str,          # Country name
    "iso_country_code": str, # ISO 3166-1 country code
    "region": str,           # Region/state name
    "iso_region_code": str,  # ISO 3166-2 region code

    # Airport Codes
    "iata": str,             # IATA airport code
    "icao": str,             # ICAO airport code

    # Location Information
    "latitude": float,       # Latitude in decimal degrees
    "longitude": float,      # Longitude in decimal degrees
    "altitude": int,         # Altitude in feet

    # Timezone Information
    "tz_name": str,          # Timezone
    "utc_offset": float,     # UTC offset
    "dst": str,              # Daylight savings region type

    # Other
    "type": str,             # Airport type
}
```

## Error Handling

The library implements robust error handling:

- Invalid IATA codes (not 3 letters) raise ValueError
- Invalid ICAO codes (not 4 letters) raise ValueError
- Invalid city codes (not 3 letters) raise ValueError
- Invalid region codes (not 4-6 characters) raise ValueError
- Invalid country codes (not 2 letters) raise ValueError

## Development

### Project Structure

```
.
├── LICENSE.txt
├── README.md
├── airports
│   ├── __init__.py
│   ├── airports.py
│   ├── data
│   │   ├── airports.json
│   │   └── incoming
│   └── merge.py
├── pyproject.toml
├── requirements-dev.txt
└── tests
    └── test_airports.py
```

### Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/airports.git
cd airports
```

2. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

3. Run tests:
```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Acknowledgments

- Data sourced from multiple airport project databases
  - [airports - Tim Rogers](https://github.com/timrogers/airports)
  - [airports-py - Aashish Vivekanand](https://github.com/aashishvanand/airports-py)