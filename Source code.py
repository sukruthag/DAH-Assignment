import concurrent.futures
import re


with open('input.txt', 'r') as f:
    words = re.findall(r'\b\w+\b', f.read())


def map_function(word):
    return (word, 1)


def reduce_function(key, values):
    return key, sum(values)

word_counts = {}


executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)


mapped_words = executor.map(map_function, words)


intermediate = {}
for key, value in mapped_words:
    if key in intermediate:
        intermediate[key].append(value)
    else:
        intermediate[key] = [value]
    # Save intermediate output
    with open(f"{key}.txt", 'a') as intermediate_file:
        intermediate_file.write(f"{key}: {value}\n")


reduced_words = executor.map(lambda key: reduce_function(key, intermediate[key]), intermediate.keys())


for key, value in reduced_words:
    word_counts[key] = value


with open('output.txt', 'w') as f:
    for key, value in word_counts.items():
        f.write(f"{key}: {value}\n")