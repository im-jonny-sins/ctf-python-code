#!/usr/bin/env python3
# rps_exploit_fixed.py
# Более устойчивый эксплойт для RPS CTF (138.197.193.132:5001)

import socket
import re
import sys
import time
import random

HOST = "138.197.193.132"
PORT = 5001
RECV_BUF = 4096
ENC = "utf-8"

# Побеждающий ход
WIN = {"R": "P", "P": "S", "S": "R",
       "r": "P", "p": "S", "s": "R"}

# Попытки предсказания из seed — возвращают один из 'R','P','S'
def predict_from_seed_try1(seed):
    # обычный python random.choice(["R","P","S"])
    random.seed(seed)
    return random.choice(["R", "P", "S"])

def predict_from_seed_try2(seed):
    # python random.randint(0,2) mapping 0->R,1->P,2->S
    random.seed(seed)
    v = random.randint(0, 2)
    return ["R", "P", "S"][v]

def predict_from_seed_try3(seed):
    # использовать getrandbits(32) затем modulo 3
    random.seed(seed)
    v = random.getrandbits(32) % 3
    return ["R", "P", "S"][v]

PREDICTORS = [predict_from_seed_try1, predict_from_seed_try2, predict_from_seed_try3]

def recv_all(sock, timeout=0.3):
    sock.settimeout(timeout)
    data = b""
    try:
        while True:
            part = sock.recv(RECV_BUF)
            if not part:
                break
            data += part
            if len(part) < RECV_BUF:
                break
    except socket.timeout:
        pass
    except Exception as e:
        print("recv error:", e)
    return data

def extract_first_number(s):
    # ищем длинное число (>=3 цифр) — чтобы не ловить года и т.п.
    m = re.search(r"(?<!\d)(\d{3,10})(?!\d)", s)
    if m:
        return int(m.group(1))
    return None

def find_explicit_choice_and_seed(s):
    # ищем "I chose X based on N"
    m = re.search(r"I chose\s*([RPSrps])\s*based on\s*(\d{1,10})", s)
    if m:
        return m.group(1).upper(), int(m.group(2))
    # ищем "based on N" (без I chose)
    m2 = re.search(r"based on\s*(\d{1,10})", s)
    if m2:
        return None, int(m2.group(1))
    return None, None

def interactive_play():
    with socket.create_connection((HOST, PORT)) as s:
        print(f"Connected to {HOST}:{PORT}")
        buffer = ""
        while True:
            data = recv_all(s, timeout=0.5)
            if data:
                try:
                    text = data.decode(ENC, errors="ignore")
                except:
                    text = data.decode("latin1", errors="ignore")
                buffer += text
                sys.stdout.write(text)
                sys.stdout.flush()

                # Если сервер явно сказал, что он выбрал + seed
                explicit_choice, seed = find_explicit_choice_and_seed(buffer)
                if explicit_choice is not None:
                    # нашли явный выбор и seed
                    bot_choice = explicit_choice
                    our_move = WIN[bot_choice]
                    s.sendall((our_move + "\n").encode(ENC))
                    print(f">>> Detected explicit bot_choice='{bot_choice}', seed={seed} -> sent: {our_move}")
                    buffer = ""
                    continue

                # Если видим только seed (например 'based on N' или просто число)
                if seed is None:
                    seed = extract_first_number(buffer)

                if seed is not None:
                    # пробуем несколько предикторов — выберем первый (можно расширить адаптацию)
                    predicted = None
                    for pred in PREDICTORS:
                        try:
                            p = pred(seed)
                        except Exception:
                            p = None
                        if p in ("R", "P", "S"):
                            predicted = p
                            break
                    if predicted is None:
                        # как запасной вариант: сопоставим seed % 3
                        predicted = ["R", "P", "S"][seed % 3]
                        reason = "fallback seed%3"
                    else:
                        reason = pred.__name__
                    our_move = WIN[predicted]
                    s.sendall((our_move + "\n").encode(ENC))
                    print(f">>> seed={seed} predicted='{predicted}' via {reason}, sent: {our_move}")
                    buffer = ""
                    continue

                # Если видим приглашение, но не смогли распарсить seed/choice — ждем дальше
                # (не отправляем "пробный" ход, чтобы не посылать случайное число)
                # Опционально можно вывести подсказку:
                if re.search(r"Please choose:.*R\s*/\s*P\s*/\s*S", buffer) or buffer.strip().endswith(">>>"):
                    # просто ждём дальнейшего вывода, который должен содержать seed или explicit choice
                    pass

            else:
                time.sleep(0.05)

if __name__ == "__main__":
    try:
        interactive_play()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print("Error:", e)
        raise
