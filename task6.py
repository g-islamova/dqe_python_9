"""
NOTE: Before running the script make sure that test file is in the same folder as this script.
You can find sample text file with records in the branch.
"""

from datetime import datetime
import os
from task6_case_mod import capitalize_first_word, normalize_text
from typing import List


class Record:
    """
    Base class for different types of record
    """

    def __init__(self, text: str):
        self.text = text


class News(Record):
    """
    Class for news records
    """

    def __init__(self, text: str, city: str):
        """
        Initialise a news record

        :param text: text content
        :param city: city associated with the news
        """
        super().__init__(text)
        self.city = capitalize_first_word(city)
        self.date = datetime.now().strftime("%d/%m/%Y %H.%M")

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        self._city = value.capitalize()

    def publish(self) -> str:
        """
        Publish news record
        """
        return f"\nNews -------------------------\n{self.text}\n{self.city}, {self.date}\n"


class PrivateAd(Record):
    """
    Class for private advertisements
    """

    def __init__(self, text: str, expiration_date: datetime):
        """
        Initialise a private advertisement record
        :param text: content of the adv
        :param expiration_date: expiration date of the adv
        """
        super().__init__(text)
        self.expiration_date = expiration_date
        self.days_left = (self.expiration_date - datetime.now()).days

    def publish(self) -> str:
        """
        Publish the private adv
        """
        normalized_text = normalize_text(self.text)
        capitalized_text = capitalize_first_word(normalized_text)
        return (f"\nPrivate Ad ------------------\n{capitalized_text}\n"
                f"Actual until: {self.expiration_date.strftime('%d/%m/%Y')}, "
                f"{self.days_left} days left\n")


class Weather(Record):
    """
    Class for weather records
    """

    def __init__(self, city: str, temperature: int):
        """
        Initialise a weather record
        :param city: city name for which weather is recorded
        :param temperature: temperature in Celsius
        """
        self.city = city
        self.temperature = temperature
        super().__init__(f"It is {temperature} in {capitalize_first_word(city)} today.")
        self.date = datetime.now().strftime("%d/%m/%Y")

    def publish(self) -> str:
        """
        Publish the notification about the weather
        """
        message = f"\nWeather today--------------\n{self.text}\n{self.date}\n"
        if self.temperature < 0:
            message += "It is cold\n"
        elif 0 <= self.temperature <= 15:
            message += "It is cool\n"
        elif 16 <= self.temperature <= 25:
            message += "It is warm\n"
        else:
            message += "It is hot\n"
        return message


class NewsFeed:
    """
    Class representing a collection of records
    """

    def __init__(self):
        self.records = []

    def add_record(self, record: Record) -> None:
        """
        Add a record to the news feed
        """
        self.records.append(record)

    def publish_feed(self) -> str:
        """
        Publish the entire news feed
        """
        output = "News feed:\n"
        for record in self.records:
            output += capitalize_first_word(normalize_text(record.publish())) + "\n"
        return output

    def save_to_file(self) -> None:
        """
        Save the news feed to a file
        """
        with open("NewsFeed.txt", "a") as file:
            for record in self.records:
                if isinstance(record, Weather):
                    file.write(record.publish())
                else:
                    file.write(capitalize_first_word(normalize_text(record.publish())) + "\n")


# Function to get user input
def get_user_input() -> Record:
    """
    Prompt user for input and create a record for news feed
    :return: Record: created news feed record
    """
    record_type = int(input("Select what you want to add: 1 - News, 2 - Private Ad, 3 - Weather: "))
    if record_type == 1 or record_type == 2:
        text = input("Insert text: ")
    if record_type == 1:
        while True:
            city = input("Insert city: ")
            if not any(char.isdigit() for char in city):  # check if city input contains digits
                break
            else:
                print("Invalid city. Please enter a valid city name.")
        return News(text, city)
    elif record_type == 2:
        while True:
            expiration_date_str = input("Insert expiration date (dd/mm/yyyy): ")
            try:
                expiration_date = datetime.strptime(expiration_date_str, "%d/%m/%Y")
                if expiration_date < datetime.now():  # check valid date
                    print("Expiration date cannot be in the past. Please enter a future date.")
                else:
                    return PrivateAd(text, expiration_date)
            except ValueError:
                print("Wrong date format. Please enter date in the format dd/mm/yyyy.")
    elif record_type == 3:
        while True:
            city = input("Insert city: ")
            if not any(char.isdigit() for char in city):  # check if city input contains digits
                break
            else:
                print("Invalid city. Please enter a valid city name.")
        while True:
            temperature_str = input("Insert temperature in Celsius: ")
            try:
                temperature = int(temperature_str)
                break
            except ValueError:
                print("Invalid temperature. Please enter a valid integer value.")
        return Weather(city, temperature)
    else:
        print("Invalid choice. Please try again.")


class TxtParser:
    def __init__(self, file_path: str = None):
        if file_path:
            self.file_path = file_path
        else:
            # Construct a universal default path based on the current working directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.file_path = os.path.join(script_dir, "news_file.txt")

    def read_records(self) -> List[str]:
        """
        Read records from the source file
        :return: List[str]: List of records read from the file
        """
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as file:
                    records = file.readlines()
                    if not records:
                        print("No records found in the source file.")
                        return []
                    return records
            else:
                print("Source file not found at the specified path or already deleted.")
                return []
        except FileNotFoundError:
            print("File not found at the specified path.")
            return []
        except IOError:
            print("An error occurred while reading the file.")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

    def write_records(self, records: List[str]) -> None:
        """
        Write records to the file
        :param records: List of records to be written
        """
        with open(self.file_path, "a") as file:
            for record in records:
                file.write(record)

    def delete_file(self) -> None:
        """
        Delete the source file after processing
        """
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            print("File not found at the specified path.")
        except Exception as e:
            print(f"An unexpected error occurred while deleting the file: {e}")

    def parse_txt(self, news_feed: NewsFeed) -> bool:
        """
        Parse the source file and add records to the news feed
        :param news_feed: NewsFeed object to add records to
        :return: bool: True if parsing is successful, False otherwise
        """
        records = self.read_records()
        if not records:
            return False

        for record in records:
            try:
                record_data = record.strip().split("|")
                if len(record_data) >= 3:  # ensure there are enough elements in the record_data
                    record_type = record_data[0].strip().lower()
                    if record_type == "news":
                        news_feed.add_record(News(record_data[1], record_data[2]))
                    elif record_type == "private ad":
                        expiration_date = datetime.strptime(record_data[2], "%d/%m/%Y")
                        news_feed.add_record(PrivateAd(record_data[1], expiration_date))
                    elif record_type == "weather":
                        news_feed.add_record(Weather(record_data[1], int(record_data[2])))
                else:
                    print(f"Unknown record type: {record_data[0]}. Skipping.")
            except IndexError:
                print("Record format is incorrect. Skipping this record.")

        self.delete_file()
        return True


def main():
    default_file_path = os.path.join(os.getcwd(), "news_file.txt")
    news_feed = NewsFeed()

    while True:
        try:
            choice = int(input("How do you want to add records? (1 - file, 2 - manual, 3 - quit): "))

            if choice == 1:
                file_choice = input("Enter path to source file or type 'skip' to process default source file: ")
                if file_choice.lower() == "skip":
                    file_path = default_file_path
                else:
                    # check if the provided file path is valid
                    if os.path.exists(file_choice):
                        file_path = file_choice
                    else:
                        print("Invalid file path. Using default file path instead.")
                        file_path = default_file_path

                txt_parser = TxtParser(file_path)
                success = txt_parser.parse_txt(news_feed)
                if success:
                    news_feed.save_to_file()
                    print("Records added from file successfully.")
                else:
                    print("No records added from file")
            elif choice == 2:
                record = get_user_input()
                if record:
                    news_feed.add_record(record)
                    news_feed.save_to_file()
                    print("Record added successfully.")
            elif choice == 3:
                break
            else:
                print("Invalid choice. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
