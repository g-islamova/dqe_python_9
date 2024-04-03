import pyodbc
from math import radians, sin, cos, sqrt, atan2
from typing import Union, Tuple, Optional


def get_coordinates(city: str) -> Optional[Union[Tuple[float, float], None, pyodbc.Row]]:
    """
    Retrieve latitude and longitude coordinates for a given city from the database.

    :param city: The name of the city
    :return: A tuple containing latitude and longitude coordinates if found.
    """
    try:
        with pyodbc.connect('DRIVER={SQLite3 ODBC Driver};'
                            'SERVER=localhost;'
                            'DATABASE=coordinates.sqlite;') as connection:
            with connection.cursor() as cursor:
                # check if city coordinates are already stored
                cursor.execute("SELECT latitude, longitude FROM city_coordinates WHERE LOWER(city)=LOWER(?)", (city,))
                result = cursor.fetchone()
                if result:
                    return result
                else:
                    print(f"Coordinates for {city.capitalize()} not found. Please provide latitude and longitude.")
                    while True:
                        try:
                            latitude = float(input("Latitude: "))
                            longitude = float(input("Longitude: "))
                            if not latitude or not longitude:
                                raise ValueError("Latitude or Longitude cannot be empty")
                            # insert new coordinates into the database
                            cursor.execute("INSERT INTO city_coordinates (city, latitude, longitude) VALUES (?, ?, ?)",
                                           (city, latitude, longitude))
                            connection.commit()
                            return latitude, longitude
                        except ValueError:
                            print("Invalid input. Latitude and Longitude must be numeric values")
    except pyodbc.Error as e:
        print(f"An error occurred with the database connection: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

        # Return None if no coordinates were found
        return None


def calculate_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calculate the straight-line distance between two sets of latitude and longitude coordinates
    using the Haversine formula.

    Variables used in Haversine formula:
    R - the radius of the Earth in km (constant value)
    a - square of half the great circle distance between the two points; intermediate value
    c - angular distance in radians on the sphere


    :param coord1: The latitude and longitude coordinates of the first city.
    :param coord2: The latitude and longitude coordinates of the second city.
    :return: The straight-line distance between the two cities in kilometers.
    """
    R = 6371.0

    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    # calculate the difference in longitude and latitude between two cities
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def main() -> None:
    """
    Main function to calculate the distance between two cities based on their coordinates.
    """
    while True:
        city1 = input("Enter first city name: ")
        if not city1:
            print("City name cannot be empty. Please enter a city name")
        else:
            break

    while True:
        city2 = input("Enter second city name: ")
        if not city2:
            print("City name cannot be empty. Please enter a city name")
        else:
            break

    coord1 = get_coordinates(city1)
    coord2 = get_coordinates(city2)

    if not coord1 or not coord2:
        print("Failed to retrieve coordinates for one or both cities.")
        return

    distance = calculate_distance(coord1, coord2)

    print(f"The straight-line distance between "
          f"{city1.capitalize()} and "
          f"{city2.capitalize()} is approximately "
          f"{distance:.2f} kilometers.")


if __name__ == "__main__":
    main()
