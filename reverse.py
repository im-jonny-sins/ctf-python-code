from itertools import permutations

input_list = [4, 54, 41, 0, 112, 32, 25, 49, 33, 3, 0, 0, 57, 32, 108, 23,
              48, 4, 9, 70, 7, 110, 36, 8, 108, 7, 49, 10, 4, 86, 43, 108,
              122, 14, 2, 71, 62, 115, 88, 78]

chars = ['J','_','o','3','t']

def score_text(s):
    # простая оценка: доля алфавита и наличие шаблонов флагов
    alpha_ratio = sum(1 for ch in s if ch.isalpha()) / len(s)
    printable_ratio = sum(1 for ch in s if 32 <= ord(ch) < 127) / len(s)
    keywords = any(k in s for k in ['picoCTF', 'CTF', 'flag', '{', '}'])
    return alpha_ratio, printable_ratio, keywords

for perm in permutations(chars):
    key_str = ''.join(perm)
    key_list = [ord(c) for c in key_str]
    # удлиняем ключ до длины входа
    while len(key_list) < len(input_list):
        key_list.extend(key_list)
    # делаем XOR
    res = ''.join(chr(a ^ b) for a, b in zip(input_list, key_list))
    alpha_ratio, printable_ratio, keywords = score_text(res)
    # печатаем только хорошие кандидаты
    if keywords or alpha_ratio > 0.5 or printable_ratio > 0.95:
        print("key =", key_str)
        print("alpha_ratio=", round(alpha_ratio,2), "printable_ratio=", round(printable_ratio,2))
        print(res)
        print("-" * 60)


