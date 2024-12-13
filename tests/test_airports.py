import json
from unittest.mock import mock_open, patch

import pytest

from airports import Airport, Airports

# Sample test data
SAMPLE_AIRPORTS = {
    "MCO": {
        "name": "Orlando International Airport",
        "iata": "MCO",
        "icao": "KMCO",
        "city": "Orlando",
        "city_code": "ORL",
        "country": "United States",
        "iso_country_code": "US",
        "region": "Florida",
        "iso_region_code": "US-FL",
        "latitude": 28.429399490356445,
        "longitude": -81.30899810791016,
    },
    "LAS": {
        "name": "McCarran International Airport",
        "iata": "LAS",
        "icao": "KLAS",
        "city": "Las Vegas",
        "city_code": "LAS",
        "country": "United States",
        "iso_country_code": "US",
        "region": "Nevada",
        "iso_region_code": "US-NV",
        "latitude": 36.08010101,
        "longitude": -115.1520004,
    },
    "JFK": {
        "name": "John F Kennedy International Airport",
        "iata": "JFK",
        "icao": "KJFK",
        "city": "New York",
        "city_code": "NYC",
        "country": "United States",
        "iso_country_code": "US",
        "region": "New York",
        "iso_region_code": "US-NY",
        "latitude": 40.63980103,
        "longitude": -73.77890015,
    },
    "LGA": {
        "name": "LaGuardia Airport",
        "iata": "LGA",
        "icao": "KLGA",
        "city": "New York",
        "city_code": "NYC",
        "country": "United States",
        "iso_country_code": "US",
        "region": "New York",
        "iso_region_code": "US-NY",
        "latitude": 40.77719879,
        "longitude": -73.87259674,
    },
}


@pytest.fixture
def mock_airports():
    """Create a mock Airports instance with test data."""
    with patch("builtins.open", mock_open(read_data=json.dumps(SAMPLE_AIRPORTS))):
        airports = Airports("mock_path.json")
        # Force data loading
        airports.data  # Access the property to trigger lazy loading
        return airports


def test_find_by_iata_code(mock_airports):
    """Test finding airport by IATA code."""
    # Test valid IATA code
    airport = mock_airports.find_by_iata_code("MCO")
    assert airport["name"] == "Orlando International Airport"
    assert airport["icao"] == "KMCO"

    # Test case insensitive
    airport = mock_airports.find_by_iata_code("mco")
    assert airport["name"] == "Orlando International Airport"

    # Test non-existent IATA code
    assert mock_airports.find_by_iata_code("XXX") is None

    # Test invalid IATA code length
    with pytest.raises(ValueError):
        mock_airports.find_by_iata_code("INVALID")


def test_find_by_icao_code(mock_airports):
    """Test finding airport by ICAO code."""
    # Test valid ICAO code
    airport = mock_airports.find_by_icao_code("KMCO")
    assert airport["name"] == "Orlando International Airport"
    assert airport["iata"] == "MCO"

    # Test case insensitive
    airport = mock_airports.find_by_icao_code("kmco")
    assert airport["name"] == "Orlando International Airport"

    # Test non-existent ICAO code
    assert mock_airports.find_by_icao_code("XXXX") is None

    # Test invalid ICAO code length
    with pytest.raises(ValueError):
        mock_airports.find_by_icao_code("KMC")


def test_find_all_by_city(mock_airports):
    """Test finding airports by city name."""
    # Test existing city with multiple airports
    ny_airports = mock_airports.find_all_by_city("New York")
    assert len(ny_airports) == 2
    assert {airport["iata"] for airport in ny_airports} == {"JFK", "LGA"}

    # Test case insensitive
    ny_airports = mock_airports.find_all_by_city("new york")
    assert len(ny_airports) == 2

    # Test city with single airport
    orlando_airports = mock_airports.find_all_by_city("Orlando")
    assert len(orlando_airports) == 1
    assert orlando_airports[0]["iata"] == "MCO"

    # Test non-existent city
    empty_airports = mock_airports.find_all_by_city("Nonexistent City")
    assert len(empty_airports) == 0


def test_find_all_by_city_code(mock_airports):
    """Test finding airports by city code."""
    # Test existing city code with multiple airports
    nyc_airports = mock_airports.find_all_by_city_code("NYC")
    assert len(nyc_airports) == 2
    assert {airport["iata"] for airport in nyc_airports} == {"JFK", "LGA"}

    # Test case insensitive
    nyc_airports = mock_airports.find_all_by_city_code("nyc")
    assert len(nyc_airports) == 2

    # Test city code with single airport
    orl_airports = mock_airports.find_all_by_city_code("ORL")
    assert len(orl_airports) == 1
    assert orl_airports[0]["iata"] == "MCO"

    # Test non-existent city code
    assert len(mock_airports.find_all_by_city_code("XXX")) == 0

    # Test invalid city code length
    with pytest.raises(ValueError):
        mock_airports.find_all_by_city_code("INVALID")


def test_find_all_by_region(mock_airports):
    """Test finding airports by region name."""
    # Test region with single airport
    fl_airports = mock_airports.find_all_by_region("Florida")
    assert len(fl_airports) == 1
    assert fl_airports[0]["iata"] == "MCO"

    # Test region with multiple airports
    ny_airports = mock_airports.find_all_by_region("New York")
    assert len(ny_airports) == 2
    assert {airport["iata"] for airport in ny_airports} == {"JFK", "LGA"}

    # Test case insensitive
    fl_airports = mock_airports.find_all_by_region("florida")
    assert len(fl_airports) == 1

    # Test non-existent region
    assert len(mock_airports.find_all_by_region("Nonexistent Region")) == 0


def test_find_all_by_region_code(mock_airports):
    """Test finding airports by region code."""
    # Test region code with single airport
    fl_airports = mock_airports.find_all_by_region_code("US-FL")
    assert len(fl_airports) == 1
    assert fl_airports[0]["iata"] == "MCO"

    # Test region code with multiple airports
    ny_airports = mock_airports.find_all_by_region_code("US-NY")
    assert len(ny_airports) == 2
    assert {airport["iata"] for airport in ny_airports} == {"JFK", "LGA"}

    # Test case insensitive
    fl_airports = mock_airports.find_all_by_region_code("us-fl")
    assert len(fl_airports) == 1

    # Test non-existent region code
    assert len(mock_airports.find_all_by_region_code("XX-XX")) == 0

    # Test invalid region code length
    with pytest.raises(ValueError):
        mock_airports.find_all_by_region_code("US")


def test_find_all_by_country(mock_airports):
    """Test finding airports by country name."""
    # Test existing country
    us_airports = mock_airports.find_all_by_country("United States")
    assert len(us_airports) == 4  # MCO, LAS, JFK, LGA
    assert {airport["iata"] for airport in us_airports} == {"MCO", "LAS", "JFK", "LGA"}

    # Test case insensitive
    us_airports = mock_airports.find_all_by_country("united states")
    assert len(us_airports) == 4

    # Test non-existent country
    assert len(mock_airports.find_all_by_country("Nonexistent Country")) == 0


def test_find_all_by_country_code(mock_airports):
    """Test finding airports by country code."""
    # Test existing country code
    us_airports = mock_airports.find_all_by_country_code("US")
    assert len(us_airports) == 4  # MCO, LAS, JFK, LGA
    assert {airport["iata"] for airport in us_airports} == {"MCO", "LAS", "JFK", "LGA"}

    # Test case insensitive
    us_airports = mock_airports.find_all_by_country_code("us")
    assert len(us_airports) == 4

    # Test non-existent country code
    assert len(mock_airports.find_all_by_country_code("XX")) == 0

    # Test invalid country code length
    with pytest.raises(ValueError):
        mock_airports.find_all_by_country_code("USA")  # 3 chars instead of 2


def test_fuzzy_find_city(mock_airports):
    """Test fuzzy city name matching."""
    # Test close match
    vegas_airports = mock_airports.fuzzy_find_city("Las Vegs")  # Intentional typo
    assert len(vegas_airports) > 0
    assert any(airport["iata"] == "LAS" for airport in vegas_airports)

    # Test no match with high cutoff
    assert len(mock_airports.fuzzy_find_city("Completely Different", cutoff=0.9)) == 0


def test_distance_between(mock_airports):
    """Test distance calculation between airports."""
    # Test distance between MCO and JFK
    distance = mock_airports.distance_between("MCO", "JFK")
    assert distance is not None
    assert 1500 < distance < 1550  # Approximate distance in km

    # Test distance between JFK and LGA (nearby airports)
    distance = mock_airports.distance_between("JFK", "LGA")
    assert distance is not None
    assert 0 < distance < 25  # Should be less than 25km apart

    # Test with one invalid airport
    assert mock_airports.distance_between("MCO", "XXX") is None

    # Test with airport dict instead of code
    mco = mock_airports.find_by_iata_code("MCO")
    jfk = mock_airports.find_by_iata_code("JFK")
    distance = mock_airports.distance_between(mco, jfk)
    assert distance is not None
    assert 1500 < distance < 1550


def test_property_getters(mock_airports):
    """Test property getter methods."""
    # Test IATA codes
    iata_codes = mock_airports.iata_codes
    assert len(iata_codes) == 4
    assert set(iata_codes) == {"MCO", "LAS", "JFK", "LGA"}

    # Test ICAO codes
    icao_codes = mock_airports.icao_codes
    assert len(icao_codes) == 4
    assert set(icao_codes) == {"KMCO", "KLAS", "KJFK", "KLGA"}

    # Test city codes
    city_codes = mock_airports.city_codes
    assert len(city_codes) == 3
    assert set(city_codes) == {"ORL", "LAS", "NYC"}


def test_airport_class():
    """Test Airport class initialization and representation."""
    airport_data = {"name": "Test Airport", "iata": "TST", "city": "Test City"}
    airport = Airport(**airport_data)

    assert airport.name == "Test Airport"
    assert airport.iata == "TST"
    assert airport.city == "Test City"
    assert str(airport) == "Airport(Test Airport, TST)"


def test_custom_data_path():
    """Test initialization with custom data path."""
    custom_path = "custom/path/airports.json"
    with patch("builtins.open", mock_open(read_data=json.dumps(SAMPLE_AIRPORTS))):
        airports = Airports(custom_path)
        assert airports._data_path == custom_path
        # Verify data loads correctly from custom path
        assert len(airports.data) == 4


def test_default_data_path():
    """Test initialization with default data path."""
    with patch("os.path.dirname") as mock_dirname:
        mock_dirname.return_value = "/mock/dir"
        airports = Airports()
        assert airports._data_path == "/mock/dir/data/airports.json"


def test_data_loading(mock_airports):
    """Test lazy loading of data."""
    # Data should be loaded when accessing the data property
    assert mock_airports._data is not None
    assert len(mock_airports.data) == 4

    # Test that lookups are built when needed
    mock_airports._ensure_lookups()
    assert mock_airports._iata_lookup is not None
    assert mock_airports._icao_lookup is not None
    assert mock_airports._city_lookup is not None
    assert mock_airports._city_code_lookup is not None
    assert mock_airports._country_lookup is not None
    assert mock_airports._country_code_lookup is not None
    assert mock_airports._region_lookup is not None
    assert mock_airports._region_code_lookup is not None
