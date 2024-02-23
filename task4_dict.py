import random
import string


def generate_list_of_dictionaries() -> list[dict[str, int]]:
    """
    Generates a list of dictionaries with random keys and values.

    Returns:
    list: A list of dictionaries.
    """
    list_of_dictionaries = []
    for _ in range(random.randint(2, 10)):
        size = random.randint(2, 10)
        keys = random.sample(string.ascii_lowercase, size)
        values = [random.randint(0, 100) for _ in range(size)]
        one_dict = dict(zip(keys, values))
        list_of_dictionaries.append(one_dict)
    return list_of_dictionaries


def merge_dicts(list_of_dicts: list[dict[str, int]]) -> dict[str, int]:
    """
    Merges a list of dictionaries into a single dictionary, retaining the maximum value for each key.

    Args:
    list_of_dicts (list): A list of dictionaries.

    Returns:
    dict: A merged dictionary.
    """
    result_dict = {}
    for idx, d in enumerate(list_of_dicts, start=0):
        for key, value in d.items():
            if key in result_dict:
                if value > result_dict[key]:
                    result_dict[key] = value
                    result_dict[key + '_' + str(idx)] = result_dict.pop(key)
            else:
                result_dict[key] = value
    return result_dict


def main():
    """
    Main function to execute the script.
    """
    list_of_dictionaries = generate_list_of_dictionaries()
    print("Generated list of dictionaries:")
    print(list_of_dictionaries)

    merged_dict = merge_dicts(list_of_dictionaries)
    print("\nMerged dictionary:")
    print(merged_dict)


if __name__ == "__main__":
    main()
