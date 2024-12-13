import json
from datetime import datetime
from zoneinfo import ZoneInfo


def get_utc_offset(tz_name):
    if not tz_name:
        return None

    try:
        tz_time = datetime.now(ZoneInfo(tz_name))
        offset_seconds = tz_time.utcoffset().total_seconds()  # type: ignore
        offset_hours = offset_seconds / 3600

        # If it's a whole number, convert to int to remove those unsightly decimal points
        if offset_hours.is_integer():
            return int(offset_hours)
        return offset_hours
    except Exception as e:
        print(f"Warning: Could not get UTC offset for timezone '{tz_name}': {str(e)}")
        return None


def create_airport_structure(airport1_data, airport2_data=None):
    """
    Create a standardized airport structure from dataset1 entry,
    optionally enhanced with dataset2 data.

    Args:
        airport1_data: Required base airport data from dataset1
        airport2_data: Optional enhancing data from dataset2
    """
    if not airport1_data:
        raise ValueError("airport1_data is required")

    # Use the appropriate source for timezone name
    tz_name = airport1_data.get("tz_name")
    if not tz_name and airport2_data:
        tz_name = airport2_data.get("time")

    return {
        # Basic Information
        "name": airport1_data["name"],
        "city": airport1_data["city"],
        "city_code": airport2_data.get("city_code") if airport2_data else None,
        "region": airport2_data.get("region_name") if airport2_data else None,
        "iso_region_code": airport2_data.get("iso_region") if airport2_data else None,
        "country": airport1_data["country"],
        "iso_country_code": (
            airport2_data.get("country_code") if airport2_data else None
        ),
        # Airport Codes
        "iata": airport1_data.get("iata"),
        "icao": airport1_data.get("icao"),
        # Location Information
        "latitude": float(
            airport1_data.get(
                "latitude", airport2_data.get("latitude") if airport2_data else None
            )
        ),
        "longitude": float(
            airport1_data.get(
                "longitude", airport2_data.get("longitude") if airport2_data else None
            )
        ),
        "altitude": float(
            airport1_data.get(
                "altitude", airport2_data.get("elevation_ft") if airport2_data else None
            )
        ),
        # Timezone Information
        "tz_name": tz_name,
        "utc_offset": get_utc_offset(tz_name) if tz_name else None,
        "dst": airport1_data.get("dst"),
        # Other
        "type": airport2_data.get("type") if airport2_data else None,
    }


def merge_airport_datasets(
    dataset1_path, dataset2_path, output_path, use_alternate=False
):
    # Load both datasets
    with open(dataset1_path, "r") as f1:
        dataset1 = json.load(f1)

    with open(dataset2_path, "r") as f2:
        dataset2 = json.load(f2)

    # Merged dataset
    merged_dataset = {}

    # Process all airports from dataset1
    for iata_code, airport1_data in dataset1.items():
        # Find corresponding airport in dataset 2
        airport2_data = next(
            (airport for airport in dataset2 if airport.get("iata") == iata_code), None
        )

        # Add IATA code to the data for completeness
        airport1_data["iata"] = iata_code

        # Create standardized structure
        merged_dataset[iata_code] = create_airport_structure(
            airport1_data=airport1_data, airport2_data=airport2_data
        )

    # Write merged dataset to output file
    with open(output_path, "w") as f_out:
        json.dump(merged_dataset, f_out, indent=4)

    print(f"Merged dataset saved to {output_path}")
    return merged_dataset


# Example usage
if __name__ == "__main__":
    merged = merge_airport_datasets(
        "data/incoming/airports-dataset-1.json",
        "data/incoming/airports-dataset-2.json",
        "data/airports.json",
    )
