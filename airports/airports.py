import json
import os
from difflib import get_close_matches
from functools import lru_cache
from typing import Dict, List, Optional, Union


class Airport:
    """
    Represents an individual airport with various attributes and lookup methods.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"Airport({self.name}, {self.iata})"  # type: ignore


class Airports:
    """
    A comprehensive library for airport data management and querying.
    """

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the Airports library.

        :param data_path: Optional custom path to airports JSON file
        """
        if data_path is None:
            # Default to a path relative to the current module
            data_path = os.path.join(os.path.dirname(__file__), "data", "airports.json")
        self._data_path = data_path

        # Lazy-loaded data structures
        self._data = None
        self._iata_lookup = None
        self._icao_lookup = None
        self._city_lookup = None
        self._city_code_lookup = None
        self._country_lookup = None
        self._country_code_lookup = None
        self._region_lookup = None
        self._region_code_lookup = None

    @property
    def data(self) -> Dict:
        """
        Lazily load and cache airport data.

        :return: Dictionary of airport data
        """
        if self._data is None:
            with open(self._data_path, "r") as f:
                self._data = json.load(f)
        return self._data

    @lru_cache(maxsize=1)
    def _build_lookups(self):
        """
        Build auxiliary lookup dictionaries for efficient querying.
        """
        iata_lookup = {}
        icao_lookup = {}
        city_lookup = {}
        city_code_lookup = {}
        region_lookup = {}
        region_code_lookup = {}
        country_lookup = {}
        country_code_lookup = {}

        for iata_code, airport_data in self.data.items():
            # IATA Lookup
            iata_lookup[iata_code] = airport_data

            # ICAO Lookup
            icao = airport_data.get("icao") or ""
            if icao:
                icao_lookup[icao] = airport_data

            # City Lookup
            city = (airport_data.get("city") or "").lower()
            if city:
                city_lookup.setdefault(city, []).append(airport_data)

            # City Code Lookup
            city_code = airport_data.get("city_code") or ""
            if city_code:
                city_code_lookup.setdefault(city_code, []).append(airport_data)

            # Region Lookup
            region = (airport_data.get("region") or "").lower()
            if region:
                region_lookup.setdefault(region, []).append(airport_data)

            # Region Code Lookup
            region_code = airport_data.get("iso_region_code") or ""
            if region_code:
                region_code_lookup.setdefault(region_code, []).append(airport_data)

            # Country Lookup
            country = (airport_data.get("country") or "").lower()
            if country:
                country_lookup.setdefault(country, []).append(airport_data)

            # Country Code Lookup
            country_code = airport_data.get("iso_country_code") or ""
            if country_code:
                country_code_lookup.setdefault(country_code, []).append(airport_data)

        return {
            "iata": iata_lookup,
            "icao": icao_lookup,
            "city": city_lookup,
            "city_code": city_code_lookup,
            "region": region_lookup,
            "region_code": region_code_lookup,
            "country": country_lookup,
            "country_code": country_code_lookup,
        }

    def _ensure_lookups(self):
        """
        Ensure lookup dictionaries are built.
        """
        if self._iata_lookup is None:
            lookups = self._build_lookups()
            self._iata_lookup = lookups["iata"]
            self._icao_lookup = lookups["icao"]
            self._city_lookup = lookups["city"]
            self._city_code_lookup = lookups["city_code"]
            self._region_lookup = lookups["region"]
            self._region_code_lookup = lookups["region_code"]
            self._country_lookup = lookups["country"]
            self._country_code_lookup = lookups["country_code"]

    def find_by_iata_code(self, iata_code: str) -> Optional[Dict]:
        """
        Find an airport by its IATA code.

        :param iata_code: 3-letter IATA airport code
        :return: Airport data or None
        """
        if not len(iata_code) == 3:
            raise ValueError("Invalid IATA code")

        self._ensure_lookups()
        return self._iata_lookup.get(iata_code.upper())  # type: ignore

    def find_by_icao_code(self, icao_code: str) -> Optional[Dict]:
        """
        Find an airport by its ICAO code.

        :param icao_code: 4-letter ICAO airport code
        :return: Airport data or None
        """
        if not len(icao_code) == 4:
            raise ValueError("Invalid ICAO code")

        self._ensure_lookups()
        return self._icao_lookup.get(icao_code.upper())  # type: ignore

    def find_all_by_city(self, city_name: str) -> List[Dict]:
        """
        Find all airports in a given city.

        :param city_name: Name of the city
        :return: List of airport data
        """
        self._ensure_lookups()
        return self._city_lookup.get(city_name.lower(), [])  # type: ignore

    def find_all_by_city_code(self, city_code: str) -> List[Dict]:
        """
        Find all airports with a specific city code.

        :param city_code: City code
        :return: List of airport data
        """
        if not len(city_code) == 3:
            raise ValueError("Invalid IATA city code")

        self._ensure_lookups()
        return self._city_code_lookup.get(city_code.upper(), [])  # type: ignore

    def find_all_by_region(self, region_name: str) -> List[Dict]:
        """
        Find all airports in a given region.

        :param region_name: Name of the region
        :return: List of airport data
        """
        self._ensure_lookups()
        return self._region_lookup.get(region_name.lower(), [])  # type: ignore

    def find_all_by_region_code(self, region_code: str) -> List[Dict]:
        """
        Find all airports with a specific region code.

        :param region_code: Region code (e.g., US-NY)
        :return: List of airport data
        """
        if not 4 <= len(region_code) <= 6:
            raise ValueError("Invalid ISO 3166-3 region code")

        self._ensure_lookups()
        return self._region_code_lookup.get(region_code.upper(), [])  # type: ignore

    def find_all_by_country(self, country_name: str) -> List[Dict]:
        """
        Find all airports in a given country.

        :param country_name: Name of the country
        :return: List of airport data
        """
        self._ensure_lookups()
        return self._country_lookup.get(country_name.lower(), [])  # type: ignore

    def find_all_by_country_code(self, country_code: str) -> List[Dict]:
        """
        Find all airports with a specific country code.

        :param country_code: Country code (e.g., US)
        :return: List of airport data
        """
        if not len(country_code) == 2:
            raise ValueError("Invalid ISO 3166 country code")

        self._ensure_lookups()
        return self._country_code_lookup.get(country_code.upper(), [])  # type: ignore

    def fuzzy_find_city(self, city_name: str, cutoff: float = 0.6) -> List[Dict]:
        """
        Find cities with names similar to the input.

        :param city_name: City name to search for
        :param cutoff: Similarity threshold
        :return: List of airport data for similar cities
        """
        self._ensure_lookups()
        similar_cities = get_close_matches(
            city_name.lower(), list(self._city_lookup.keys()), cutoff=cutoff  # type: ignore
        )

        results = []
        for city in similar_cities:
            results.extend(self._city_lookup[city])  # type: ignore

        return results

    @property
    def iata_codes(self) -> List[str]:
        """
        Get all IATA codes in the dataset.

        :return: List of IATA codes
        """
        return list(self.data.keys())

    @property
    def icao_codes(self) -> List[str]:
        """
        Get all ICAO codes in the dataset.

        :return: List of ICAO codes
        """
        self._ensure_lookups()
        return list(self._icao_lookup.keys())  # type: ignore

    @property
    def city_codes(self) -> List[str]:
        """
        Get all IATA city codes in the dataset.

        :return: List of IATA city codes
        """
        self._ensure_lookups()
        return list(self._city_code_lookup.keys())  # type: ignore

    def distance_between(
        self, airport1: Union[str, Dict], airport2: Union[str, Dict]
    ) -> Optional[float]:
        """
        Calculate distance between two airports.

        :param airport1: First airport (IATA code or airport data)
        :param airport2: Second airport (IATA code or airport data)
        :return: Distance in kilometers or None
        """
        from math import atan2, cos, radians, sin, sqrt

        def get_airport_coords(airport):
            if isinstance(airport, str):
                airport = self.find_by_iata_code(airport)

            if not airport:
                return None

            lat = airport.get("latitude")
            lon = airport.get("longitude")
            if lat is None or lon is None:
                return None

            return (lat, lon)

        # Earth's radius in kilometers
        R = 6371.0

        # Get coordinates
        coords1 = get_airport_coords(airport1)
        coords2 = get_airport_coords(airport2)

        if not coords1 or not coords2:
            return None

        lat1, lon1 = map(radians, coords1)
        lat2, lon2 = map(radians, coords2)

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c


# Example usage
if __name__ == "__main__":
    airports = Airports()

    # Example queries
    mco = airports.find_by_iata_code("MCO")
    print("Orlando International Airport:")
    print("\n", json.dumps(mco, indent=4))

    lv_airports = airports.find_all_by_city("Las Vegas")
    print("\nLas Vegas Airports:")
    print("\n", json.dumps(lv_airports, indent=4))

    nycc_airports = airports.find_all_by_city_code("NYC")
    print("\nNYC City Code Airports:")
    print("\n", json.dumps(nycc_airports, indent=4))

    us_airports = airports.find_all_by_country("United States")
    print("\nUS Airports Count:", len(us_airports))
