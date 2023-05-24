import random
import string
import collections
import math

import chardet as chardet
from matplotlib import pyplot as plt

def parameters(s):
    counter = collections.Counter(s)
    prob = {symbol: count / len(s) for symbol, count in counter.items()}
    prob_str = ', '.join([f"{symbol}={prob:.2f}" for symbol, prob in prob.items()])
    main_prob = sum(prob.values()) / len(prob)
    equal = all(abs(prob - main_prob) < 0.05 * main_prob for prob in prob.values())
    uniformity = "рівна" if equal == main_prob else "нерівна"
    entropy = round(-sum(p * math.log2(p) for p in prob.values()), 2)
    source_excess = round((1 - entropy / math.log2(len(set(s)))) if len(set(s)) > 1 else 1, 2)
    main_prob = round(main_prob, 2)
    return prob_str, main_prob, uniformity, entropy, source_excess

def lossless_comp():

    global aray

    text = open('results_sequence.txt', 'w')
    N_sequence = 100
    N1 = 2
    arr1 = [1] * N1
    N0 = N_sequence - N1
    arr0 = [0] * N0
    results = []
    origin_seq_1 = arr1 + arr0
    random.shuffle(origin_seq_1)
    origin_seq_1 = ''.join(map(str, origin_seq_1))
    text.write(f'Варіант: 2\n')
    text.write(f'Завдання 1\n')
    text.write('Послідовність: ' + str(origin_seq_1) + '\n')
    original_sequence_size = len(origin_seq_1)
    text.write('Розмір послідовності: ' + str(original_sequence_size) + ' byte' + '\n')
    unique_chars = set(origin_seq_1)
    seq_size_alphabet = len(unique_chars)
    text.write('Розмір алфавіту: ' + str(seq_size_alphabet) + '\n')
    probability_str, mean_probability, uniformity, entropy, source_excess = parameters(origin_seq_1)
    results.append([seq_size_alphabet, round(entropy, 2), round(source_excess, 2), uniformity])
    text = open('results_sequence.txt', 'a')
    text.write(f'Ймовірність появи символів: {probability_str}\n')
    text.write(f'Середнє арифметичне ймовірності: {mean_probability}\n')
    text.write(f'Ймовірність розподілу символів: {uniformity}\n')
    text.write(f'Ентропія: {entropy}\n')
    text.write(f'Надмірність джерела: {source_excess}\n')
    text.write('\n')


    N2 = 8
    list2 = ['а', 'п', 'а', 'н', 'а', 'с', 'ю', 'к']
    origin_seq_2 = ''.join(list2 + [str(0)] * (N_sequence - N2))
    text.write('Завдання 2\n')
    text.write(f'Послідовність: {origin_seq_2}\n')
    text.write(f'Розмір послідовності: {len(origin_seq_2)} byte\n')
    seq_size_alphabet = len(set(origin_seq_2))
    text.write(f'Розмір алфавіту: {seq_size_alphabet}\n')

    probability_str, mean_probability, uniformity, entropy, source_excess = parameters(origin_seq_2)
    results.append([seq_size_alphabet, round(entropy, 2), round(source_excess, 2), uniformity])
    text.write(f'Ймовірність появи символів: {probability_str}\n')
    text.write(f'Середнє арифметичне ймовірності: {mean_probability}\n')
    text.write(f'Ймовірність розподілу символів: {uniformity}\n')
    text.write(f'Ентропія: {entropy}\n')
    text.write(f'Надмірність джерела: {source_excess}\n')
    text.write('\n')


    origin_seq_3 = list(origin_seq_2)
    random.shuffle(origin_seq_3)
    origin_seq_3 = ''.join(map(str, origin_seq_3))
    text.write(f'Завдання 3\n')
    text.write('Послідовність: ' + str(origin_seq_3) + '\n')
    text.write('Розмір послідовності: ' + str(len(origin_seq_3)) + ' byte' + '\n')
    unique_chars = set(origin_seq_3)
    seq_size_alphabet = len(unique_chars)
    text.write('Розмір алфавіту: ' + str(seq_size_alphabet) + '\n')

    probability_str, mean_probability, uniformity, entropy, source_excess = parameters(origin_seq_3)
    results.append([seq_size_alphabet, round(entropy, 2), round(source_excess, 2), uniformity])

    text = open('results_sequence.txt', 'a')
    text.write(f'Ймовірність появи символів: {probability_str}\n')
    text.write(f'Середнє арифметичне ймовірності: {mean_probability}\n')
    text.write(f'Ймовірність розподілу символів: {uniformity}\n')
    text.write(f'Ентропія: {entropy}\n')
    text.write(f'Надмірність джерела: {source_excess}\n')
    text.write('\n')

    aray = []
    letters = ['а', 'п', 'р', 'н', 'а', 'с', 'ю', 'к', '5', '1', '9', 'c', 'т']
    n_letters = len(letters)
    n_repeats = N_sequence / n_letters
    remainder = N_sequence * (N_sequence % n_letters)
    aray += letters * int(n_repeats)
    aray += letters[:remainder]
    origin_seq_4 = ''.join(map(str, aray))
    text.write(f'Завдання 4\n')
    text.write('Послідовність: ' + origin_seq_4 + '\n')
    text.write('Розмір послідовності: ' + str(len(origin_seq_4)) + ' byte' + '\n')
    unique_chars = set(origin_seq_4)
    seq_size_alphabet = len(unique_chars)
    text.write('Розмір алфавіту: ' + str(seq_size_alphabet) + '\n')

    probability_str, mean_probability, uniformity, entropy, source_excess = parameters(origin_seq_4)
    results.append([seq_size_alphabet, round(entropy, 2), round(source_excess, 2), uniformity])

    text = open('results_sequence.txt', 'a')
    text.write(f'Завдання 4\n')
    text.write(f'Ймовірність появи символів: {probability_str}\n')
    text.write(f'Середнє арифметичне ймовірності: {mean_probability}\n')
    text.write(f'Ймовірність розподілу символів: {uniformity}\n')
    text.write(f'Ентропія: {entropy}\n')
    text.write(f'Надмірність джерела: {source_excess}\n')
    text.write('\n')

    alphabet = ['а', 'п', '5', '1', '9']
    Pi = 0.2
    length = Pi * N_sequence
    origin_seq_5 = alphabet * int(length)
    random.shuffle(origin_seq_5)
    origin_seq_5 = ''.join(map(str, origin_seq_5))
    text.write(f'Завдання 5\n')
    text.write('Послідовність: ' + str(origin_seq_5) + '\n')
    text.write('Розмір послідовності: ' + str(len(origin_seq_5)) + ' byte' + '\n')
    unique_chars = set(origin_seq_5)
    seq_size_alphabet = len(unique_chars)
    text.write('Розмір алфавіту: ' + str(seq_size_alphabet) + '\n')

    counts = collections.Counter(origin_seq_5)
    probability = {symbol: count / N_sequence for symbol, count in counts.items()}
    probability_str = ', '.join([f"{symbol}={prob:.4f}" for symbol, prob in probability.items()])
    mean_probability = sum(probability.values()) / len(probability)
    equal = all(abs(prob - mean_probability) < 0.05 * mean_probability for prob in probability.values())
    if equal:
        uniformity = "рівна"
    else:
        uniformity = "нерівна"
    entropy = -sum(p * math.log2(p) for p in probability.values())
    if seq_size_alphabet > 1:
        source_excess = 1 - entropy / math.log2(seq_size_alphabet)
    else:
        source_excess = 1
    results.append([seq_size_alphabet, round(entropy, 2), round(source_excess, 2), uniformity])

    text = open('results_sequence.txt', 'a')
    text.write(f'Ймовірність появи символів: {probability_str}\n')
    text.write(f'Середнє арифметичне ймовірності: {mean_probability}\n')
    text.write(f'Ймовірність розподілу символів: {uniformity}\n')
    text.write(f'Ентропія: {entropy}\n')
    text.write(f'Надмірність джерела: {source_excess}\n')
    text.write('\n')


    list_letters = ['а', 'п']
    list_digits = ['5', '1', '9']
    P_letters = 0.7
    P_digits = 0.3
    n_letters6 = int(P_letters * N_sequence) / len(list_letters)
    n_digits6 = int(P_digits * N_sequence) / len(list_digits)
    list_l = list_letters * int(n_letters6)
    list_d = list_digits * int(n_digits6)
    origin_seq_6 = list_l + list_d
    random.shuffle(origin_seq_6)
    origin_seq_6 = ''.join(map(str, origin_seq_6))
    text.write(f'Завдання 6\n')
    text.write('Послідовність: ' + str(origin_seq_6) + '\n')
    text.write('Розмір послідовності: ' + str(len(origin_seq_6)) + ' byte' + '\n')
    unique_chars = set(origin_seq_6)
    seq_size_alphabet = len(unique_chars)
    text.write('Розмір алфавіту: ' + str(seq_size_alphabet) + '\n')

    probability_str, mean_probability, uniformity, entropy, source_excess = parameters(origin_seq_6)
    results.append([seq_size_alphabet, round(entropy, 2), round(source_excess, 2), uniformity])

    text = open('results_sequence.txt', 'a')
    text.write(f'Ймовірність появи символів: {probability_str}\n')
    text.write(f'Середнє арифметичне ймовірності: {mean_probability}\n')
    text.write(f'Ймовірність розподілу символів: {uniformity}\n')
    text.write(f'Ентропія: {entropy}\n')
    text.write(f'Надмірність джерела: {source_excess}\n')
    text.write('\n')

    elements = string.ascii_lowercase + string.digits
    origin_seq_7 = [random.choice(elements) for _ in range(N_sequence)]
    origin_seq_7 = ''.join(map(str, origin_seq_7))
    text.write('Послідовність: ' + str(origin_seq_7) + '\n')
    text.write('Розмір послідовності: ' + str(len(origin_seq_7)) + ' byte' + '\n')
    unique_chars = set(origin_seq_7)
    seq_size_alphabet = len(unique_chars)
    text.write(f'Завдання 7\n')
    text.write('Розмір алфавіту: ' + str(seq_size_alphabet) + '\n')

    probability_str, mean_probability, uniformity, entropy, source_excess = parameters(origin_seq_7)
    results.append([seq_size_alphabet, round(entropy, 2), round(source_excess, 2), uniformity])

    text = open('results_sequence.txt', 'a')
    text.write(f'Ймовірність появи символів: {probability_str}\n')
    text.write(f'Середнє арифметичне ймовірності: {mean_probability}\n')
    text.write(f'Ймовірність розподілу символів: {uniformity}\n')
    text.write(f'Ентропія: {entropy}\n')
    text.write(f'Надмірність джерела: {source_excess}\n')
    text.write('\n')

    origin_seq_8 = ['1'] * N_sequence
    origin_seq_8 = ''.join(map(str, origin_seq_8))
    text.write(f'Завдання 8\n')
    text.write('Послідовність: ' + str(origin_seq_8) + '\n')
    text.write('Розмір послідовності: ' + str(len(origin_seq_8)) + ' byte' + '\n')
    unique_chars = set(origin_seq_8)
    seq_size_alphabet = len(unique_chars)
    text.write('Розмір алфавіту: ' + str(seq_size_alphabet) + '\n')

    probability_str, mean_probability, uniformity, entropy, source_excess = parameters(origin_seq_8)
    results.append([seq_size_alphabet, round(entropy, 2), round(source_excess, 2), uniformity])

    text = open('results_sequence.txt', 'a')
    text.write(f'Ймовірність появи символів: {probability_str}\n')
    text.write(f'Середнє арифметичне ймовірності: {mean_probability}\n')
    text.write(f'Ймовірність розподілу символів: {uniformity}\n')
    text.write(f'Ентропія: {entropy}\n')
    text.write(f'Надмірність джерела: {source_excess}\n')
    text.write('\n')

    text.close()

    sequence_file = open('sequence.txt', 'w')
    original_sequences = [origin_seq_1, origin_seq_2, origin_seq_3, origin_seq_4,
                          origin_seq_5, origin_seq_6, origin_seq_7, origin_seq_8]
    sequence_file.write(str(original_sequences))
    sequence_file.close()

    text.close()

    text.close()

    fig, ax = plt.subplots(figsize=(14 / 1.54, 8 / 1.54))
    plt.title("Характеристика сформованих послідовностей")
    headers = ['Розмір алфавіту', 'Ентропія', 'Надмірність', 'Ймовірність']
    row = ['Послідовність 1', 'Послідовність 2', 'Послідовність 3', 'Послідовність 4', 'Послідовність 5',
           'Послідовність 6', 'Послідовність 7', 'Послідовність 8']
    ax.axis('off')
    table = ax.table(cellText=results, colLabels=headers, rowLabels=row, loc='center', cellLoc='center')
    table.set_fontsize(14)
    table.scale(0.8, 2)
    fig.savefig('Характеристика сформованих послідовностей' + '.png')

    with open("results_sequence.txt", "rb") as f:
        data = f.read()
    result = chardet.detect(data)
    encoding = result['encoding']
    with open("results_sequence.txt", "r", encoding=encoding) as f:
        data = f.read()
    with open("results_sequence.txt", "w", encoding='utf-8') as f:
        f.write(data)

lossless_comp()