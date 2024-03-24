"""
NOTE: Before running the script make sure that test file is in the folder named "xml_fies"
and that folder is placed in the same folder as this script.
You can find sample xml file with records in the branch.
"""

import csv
import json
import os
from collections import Counter
import xml.etree.ElementTree as eT
from datetime import datetime
from typing import List
from task9_imp_module import capitalize_first_word, normalize_text


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
        return f"News -------------------------\n{self.text}\n{self.city}, {self.date}\n"


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
        return (f"Private Ad ------------------\n{capitalized_text}\n"
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
        self.city = capitalize_first_word(city)  # capitalize city before initializing the superclass
        self.temperature = temperature
        super().__init__(f"It is {temperature} in {self.city} today.")  # using self.city
        self.date = datetime.now().strftime("%d/%m/%Y")

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        self._city = capitalize_first_word(value)

    def publish(self) -> str:
        """
        Publish the notification about the weather
        """
        message = f"Weather today--------------\nIt is {self.temperature} in {self.city} today.\n{self.date}\n"
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
        self.word_counts: Counter = Counter()
        self.letter_counts: Counter = Counter()
        self.total_letters = 0
        self.total_uppercase_letters: dict = {}  # Initialize as an empty dictionary

    def add_record(self, record: Record) -> None:
        """
        Add a record to the news feed
        """
        self.records.append(record)
        self.count_words(record.text)
        self.count_letters(record.text)

    def count_words(self, text):
        """
        Count words in the text and update word counts
        """
        words = text.lower().split()
        self.word_counts.update(words)

    def count_letters(self, text):
        """
        Count letters in the text and update letter counts
        :param text: Text to count letters from
        """
        text_lower = text.lower()
        self.total_letters = sum(1 for char in text_lower if char.isalpha())

        for char in text:
            if char.isalpha():  # consider only alphabetic characters
                # count all letters lower and upper
                char_lower = char.lower()
                self.letter_counts[char_lower] = self.letter_counts.get(char_lower, 0) + 1
                if char.isupper():
                    self.total_uppercase_letters[char_lower] = self.total_uppercase_letters.get(char_lower, 0) + 1

    def save_cnt_words(self, filename):
        with open(filename, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter='-')
            for word, count in self.word_counts.items():
                writer.writerow([word, count])

    def save_cnt_letters(self, filename):
        """
        Save letter counts to a CSV file
        :param filename: Name of the CSV file
        """
        with open(filename, 'w', newline='') as csvfile:
            headers = ["letter", "count_all", "count_uppercase", "percentage"]
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for letter, total_count in self.letter_counts.items():
                total_percentage = (total_count / self.total_letters) * 100 if self.total_letters > 0 else 0
                uppercase_count = self.total_uppercase_letters.get(letter, 0)
                writer.writerow({
                    "letter": letter,
                    "count_all": total_count,
                    "count_uppercase": uppercase_count,
                    "percentage": f"{total_percentage:.2f}%"
                })

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


class JsonParser:
    def __init__(self, folder_path: str = None):
        if folder_path:
            self.folder_path = folder_path
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.folder_path = os.path.join(script_dir, "json_files")

    def read_records(self) -> list:
        """
        Reads records from JSON files in the specified folder.
        Returns a list of records.
        """
        records = []
        try:
            if os.path.exists(self.folder_path):
                files = [f for f in os.listdir(self.folder_path) if f.endswith('.json')]
                if not files:
                    print("No JSON files found in the specified folder.")
                    return records
                else:
                    for file_name in files:
                        with open(os.path.join(self.folder_path, file_name), "r") as file:
                            data = json.load(file)
                            if isinstance(data, list):
                                records.extend(data)
                            else:
                                print("Invalid JSON format in file:", file_name)
                return records
            else:
                print("Folder not found at the specified path.")
                return records
        except FileNotFoundError:
            print("Folder not found at the specified path.")
            return records
        except IOError:
            print("An error occurred while reading the JSON files.")
            return records
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return records

    def write_records(self, records: list) -> bool:
        """
        Writes records to JSON files in the specified folder.
        Returns True if writing is successful, False otherwise.
        """
        try:
            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)
            for i, record in enumerate(records):
                file_path = os.path.join(self.folder_path, f"record_{i}.json")
                with open(file_path, "w") as file:
                    json.dump(record, file, indent=4)
            return True
        except IOError:
            print("An error occurred while writing the JSON files.")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def delete_file(self, file_name: str) -> bool:
        """
        Deletes the specified file from the folder.
        Returns True if deletion is successful, False otherwise.
        """
        try:
            file_path = os.path.join(self.folder_path, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            else:
                print("File not found:", file_name)
                return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def parse_json(self, news_feed: NewsFeed, data: list) -> bool:
        """
        Parses JSON data and adds records to the news feed.
        Returns True if parsing is successful, False otherwise.
        """
        try:
            for record in data:
                try:
                    record_type = record.get("type", "").strip().lower()
                    if record_type == "news":
                        news_feed.add_record(News(record["text"], record["city"]))
                    elif record_type == "private ad":
                        expiration_date = datetime.strptime(record["expiration_date"], "%d/%m/%Y")
                        news_feed.add_record(PrivateAd(record["text"], expiration_date))
                    elif record_type == "weather":
                        news_feed.add_record(Weather(record["city"], record["temperature"]))
                except KeyError:
                    print("Record format is incorrect. Skipping this record.")
            return True
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False


class XmlParser:
    def __init__(self, folder_path: str = None):
        if folder_path:
            self.folder_path = folder_path
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.folder_path = os.path.join(script_dir, "xml_files")

    def read_records(self) -> list:
        records = []
        try:
            if os.path.exists(self.folder_path):
                files = [f for f in os.listdir(self.folder_path) if f.endswith('.xml')]
                if not files:
                    print("No XML files found in the specified folder.")
                    return records
                else:
                    for file_name in files:
                        tree = eT.parse(os.path.join(self.folder_path, file_name))
                        root = tree.getroot()
                        for record in root.findall('record'):
                            record_data = {}
                            for child in record:
                                record_data[child.tag] = child.text
                            records.append(record_data)
                return records
            else:
                print("Folder not found at the specified path.")
                return records
        except FileNotFoundError:
            print("Folder not found at the specified path.")
            return records
        except IOError:
            print("An error occurred while reading the XML files.")
            return records
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return records

    def write_records(self, records: list) -> bool:
        """
        Writes records to XML files in the specified folder.
        Returns True if writing is successful, False otherwise.
        """
        try:
            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)
            for i, record in enumerate(records):
                root = eT.Element("records")
                record_element = eT.SubElement(root, "record")
                for key, value in record.items():
                    child = eT.SubElement(record_element, key)
                    child.text = str(value)
                tree = eT.ElementTree(root)
                file_path = os.path.join(self.folder_path, f"record_{i}.xml")
                tree.write(file_path)
            return True
        except IOError:
            print("An error occurred while writing the XML files.")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def delete_file(self, file_name: str) -> bool:
        """
        Deletes the specified file from the folder.
        Returns True if deletion is successful, False otherwise.
        """
        try:
            file_path = os.path.join(self.folder_path, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            else:
                print("File not found:", file_name)
                return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def parse_xml(self, news_feed: NewsFeed, data: list) -> bool:
        """
        Parses XML data and adds records to the news feed.
        Returns True if parsing is successful, False otherwise.
        """
        try:
            for record_data in data:
                record_type = record_data.get("type", "").strip().lower()
                if record_type == "news":
                    news_feed.add_record(News(record_data["text"], record_data["city"]))
                elif record_type == "private ad":
                    expiration_date = datetime.strptime(record_data["expiration_date"], "%d/%m/%Y")
                    news_feed.add_record(PrivateAd(record_data["text"], expiration_date))
                elif record_type == "weather":
                    news_feed.add_record(Weather(record_data["city"], int(record_data["temperature"])))
            return True
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False


def main():
    default_file_path = os.path.join(os.getcwd(), "news_file.txt")
    default_folder_path = os.path.join(os.getcwd(), "json_files")
    default_folder_path_xml = os.path.join(os.getcwd(), "xml_files")
    news_feed = NewsFeed()

    while True:
        try:
            choice = int(input("How do you want to add records? "
                               "(1 - file (txt), "
                               "2 - file (json), "
                               "3 - file (xml), "
                               "4 - manual, "
                               "5 - quit): "))

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
                folder_choice = input("Enter folder path containing JSON files or type 'skip' to use default folder: ")
                if folder_choice.lower() == "skip":
                    folder_path = default_folder_path
                else:
                    # check if the provided folder path is valid
                    if os.path.exists(folder_choice):
                        folder_path = folder_choice
                    else:
                        print("Invalid folder path. Using default folder path instead.")
                        folder_path = default_folder_path

                json_parser = JsonParser(folder_path)
                data = json_parser.read_records()
                if data:
                    success = json_parser.parse_json(news_feed, data)
                    if success:
                        news_feed.save_to_file()
                        print("Records added from JSON files successfully.")
                        for file_name in os.listdir(folder_path):
                            if file_name.endswith('.json'):
                                json_parser.delete_file(file_name)
                    else:
                        print("No records added from JSON files.")
            elif choice == 3:  # New option for XML files
                folder_choice = input("Enter folder path containing XML files or type 'skip' to use default folder: ")
                if folder_choice.lower() == "skip":
                    folder_path = default_folder_path_xml
                else:
                    # check if the provided folder path is valid
                    if os.path.exists(folder_choice):
                        folder_path = folder_choice
                    else:
                        print("Invalid folder path. Using default folder path instead.")
                        folder_path = default_folder_path_xml

                xml_parser = XmlParser(folder_path)
                data = xml_parser.read_records()
                if data:
                    success = xml_parser.parse_xml(news_feed, data)
                    if success:
                        news_feed.save_to_file()
                        print("Records added from XML files successfully.")
                        for file_name in os.listdir(folder_path):
                            if file_name.endswith('.xml'):
                                xml_parser.delete_file(file_name)
                    else:
                        print("No records added from XML files.")
            elif choice == 4:
                record = get_user_input()
                if record:
                    news_feed.add_record(record)
                    news_feed.save_to_file()
                    print("Record added successfully.")
            elif choice == 5:
                break
            else:
                print("Invalid choice. Please try again.")

            news_feed.save_cnt_words("word_counts.csv")
            news_feed.save_cnt_letters("letter_counts.csv")

        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
