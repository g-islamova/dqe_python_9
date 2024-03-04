from datetime import datetime


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
        self.city = city.capitalize()
        self.date = datetime.now().strftime("%d/%m/%Y %H.%M")

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
        return (f"Private Ad ------------------\n{self.text}\n"
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
        self.city = city.capitalize()
        self.temperature = temperature
        text = f"It is {self.temperature} in {self.city} today."
        super().__init__(text)
        self.date = datetime.now().strftime("%d/%m/%Y")

    def publish(self) -> str:
        """
        Publish the notification about the weather
        """
        message = f"Weather today--------------\n{self.text}\n{self.date}\n"
        if self.temperature < 0:
            message += "It is cold"
        elif 0 <= self.temperature <= 15:
            message += "It is cool"
        elif 16 <= self.temperature <= 25:
            message += "It is warm"
        else:
            message += "It is hot"
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
            output += record.publish() + "\n"
        return output

    def save_to_file(self) -> None:
        """
        Save the news feed to a file
        """
        with open("NewsFeed.txt", "a") as file:
            file.write(self.publish_feed() + "\n")


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
            if not city.strip().isdigit():  # check if city input is not a number
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
            if not city.strip().isdigit():  # Check if city input is not a number
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
        return None


# example usage:
news_feed = NewsFeed()

# get user input and add record
record = get_user_input()
if record:
    news_feed.add_record(record)

# save news feed to file
news_feed.save_to_file()
