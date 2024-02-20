import re

text_to_format = """
homEwork:
	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

#  define a regex that matches the first word of a sentence
p = re.compile(r'(?<=[.?!:\n]\s)(\w+)')


# function to capitalize the first letter of each sentence
def cap(match):
    return match.group(0).capitalize()


# normalise the text to lowercase, fix misspelling
homework_text_normalized = text_to_format.lower().replace(" iz ", " is ")


# substitute lowercase letters with capital ones in the text
result = p.sub(cap, homework_text_normalized)

# calculate number of whitespace characters
whitespace_count = sum(1 for char in text_to_format if char in ' \t\n')

# create a list of sentences
sentences = [sentence.strip() for sentence in homework_text_normalized.split('.') if sentence.strip()]

# Get last words from each sentence
last_words = [sentence.split()[-1] for sentence in sentences]

# Create a new sentence with last words
new_sentence = " ".join(last_words) + "."

# Add the new sentence to the end of the paragraph
result += "\n\n" + new_sentence.capitalize()

# Output the results
print("Normalised text:\n", result)
print("\nNumber of whitespace characters:", whitespace_count)
