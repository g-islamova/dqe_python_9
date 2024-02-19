import random
import string

# declare var to store resulting set of dicts
list_of_dictionaries = []
for _ in range(random.randint(2, 10)):
    # define random number od dictionaries
    size = random.randint(2, 10)
    # get random letters for keys w/o duplicates
    keys = random.sample(string.ascii_lowercase, size)
    # get random numbers for values
    values = [random.randint(0, 100) for _ in range(size)]
    # construct one dictionary
    one_dict = dict(zip(keys, values))
    # merge created dictionaries into list
    list_of_dictionaries.append(one_dict)
print(list_of_dictionaries)


# function to merge dictionaries
def merge_dicts(list_of_dicts):
    result_dict = {}
    # start iteration over each dict in the list
    for idx, d in enumerate(list_of_dicts, start=0):
        # start iteration over each key-value pair in each dict
        for key, value in d.items():
            # check if key already exists in merged_dict
            if key in result_dict:
                # if key exists, compare its value with the current key and
                # update the value if new value is greater
                # rename the key with the index, previous key removed
                if value > result_dict[key]:
                    result_dict[key] = value
                    result_dict[key + '_' + str(idx)] = result_dict.pop(key)
            # if key does not exist, add key-value pair from current dict
            else:
                result_dict[key] = value
    return result_dict


# merge the list of dictionaries
merged_dict = merge_dicts(list_of_dictionaries)

# print the merged dictionary
print(merged_dict)
