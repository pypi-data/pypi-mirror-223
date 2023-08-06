def get_string_between_2_substrings(input_string, start_substring, end_substring, remove_space):
    input_string = str(input_string)
    start_index = input_string.find(start_substring)

    if not start_index or start_index == -1:
        return None

    start_index += len(start_substring)
    end_index = input_string.find(end_substring, start_index)

    if not end_index or end_index == -1:
        return None

    if remove_space:
        string = input_string[start_index:end_index]
        string.replace(" ", "")
        return string

    else:
        return input_string[start_index:end_index]


def get_string_between_substring_and_end(input_string, start_substring, remove_space):
    input_string = str(input_string)
    start_index = input_string.find(start_substring)

    if not start_index or start_index == -1:
        return None
    else:

        start_index += len(start_substring)
        end_index = len(input_string)

        if remove_space:
            string = input_string[start_index:end_index]
            string.replace(" ", "")
            return string
        else:
            return input_string[start_index:end_index]


def get_string_between_last_substring_and_end(input_string, start_substring, remove_space):
    input_string = str(input_string)
    start_index = input_string.rfind(start_substring)

    if not start_index or start_index == -1:
        return None
    else:

        start_index += len(start_substring)
        end_index = len(input_string)

        if remove_space:
            string = input_string[start_index:end_index]
            string.replace(" ", "")
            return string
        else:
            return input_string[start_index:end_index]