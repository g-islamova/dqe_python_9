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


def merge_dicts(list_of_dicts):
    result_dict = {}
    # iterate over each dict in the list
    for idx, d in enumerate(list_of_dicts, start=0):
        # iterate over each key-value pair in each dict
        for key, value in d.items():
            # check if key already exists in result_dict
            if key in result_dict:
                # if value in current dict is greater, update result_dict
                if value > result_dict[key][0]:
                    result_dict[key] = (value, idx)
            else:
                # if key doesn't exist, add key-value pair to result_dict
                result_dict[key] = (value, idx)

    # compile the final dictionary with renamed keys
    final_dict = {}
    for key, (value, idx) in result_dict.items():
        if idx == 0:
            final_dict[key] = value
        else:
            final_dict[f"{key}_{idx}"] = value

    return final_dict


merged_dict = merge_dicts(list_of_dictionaries)

print(merged_dict)
