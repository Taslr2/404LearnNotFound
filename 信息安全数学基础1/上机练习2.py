import random
from math import gcd

def is_primitive_root(g, p, factors_p_minus_1):
    if gcd(g, p) != 1:
        return False
    for q in factors_p_minus_1:
        if pow(g, (p - 1) // q, p) == 1:
            return False
    return True

def get_prime_factors(n):
    factors = set()
    d = 2
    temp_n = n
    while d * d <= temp_n:
        if temp_n % d == 0:
            factors.add(d)
            while temp_n % d == 0:
                temp_n //= d
        d += 1
    if temp_n > 1:
        factors.add(temp_n)
    return list(factors)

def find_primitive_root(p):
    if p == 2:
        return 1
    p_minus_1 = p - 1
    prime_factors_p_minus_1 = get_prime_factors(p_minus_1)

    for g in range(2, p):
        if is_primitive_root(g, p, prime_factors_p_minus_1):
            return g
    return None 

def power(a, b, m):
    res = 1
    a %= m
    while b > 0:
        if b % 2 == 1:
            res = (res * a) % m
        a = (a * a) % m
        b //= 2
    return res

def modInverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1


p = 2357
print(f"选择的素数 p = {p}")

alpha = find_primitive_root(p)
if alpha is None:
    print(f"未能找到模 {p} 的本原元。请检查素数 p。")
    exit()
print(f"找到的本原元 α = {alpha}")

a = random.randint(2, p - 2)
print(f"选择的私钥 a = {a}")

beta = power(alpha, a, p)
print(f"计算得到的公钥 β = {beta}")
print(f"公钥: (p={p}, α={alpha}, β={beta})")
print(f"私钥: a={a}")

print("-" * 30)

m = random.randint(0, p - 1)
print(f"选择的随机消息 m = {m}")

r = random.randint(2, p - 2)
print(f"选择的随机数 r = {r}")

c1 = power(alpha, r, p)

c2 = (m * power(beta, r, p)) % p
print(f"计算得到的密文 (c1, c2) = ({c1}, {c2})")

print("-" * 30)


s = power(c1, a, p)

s_inv = modInverse(s, p)

m_prime = (c2 * s_inv) % p
print(f"解密计算得到的 s = c1^a mod p = {s}")
print(f"解密计算得到的 s 的逆元 s_inv = {s_inv}")
print(f"解密得到的明文 m' = {m_prime}")


if m == m_prime:
    print("解密成功！明文 m' 与原始消息 m 一致。")
else:
    print("解密失败！明文 m' 与原始消息 m 不一致。")

def is_primitive_root(g, p, factors_p_minus_1):
    if gcd(g, p) != 1:
        return False
    for q in factors_p_minus_1:
        if pow(g, (p - 1) // q, p) == 1:
            return False
    return True

def get_prime_factors(n):
    factors = set()
    d = 2
    temp_n = n
    while d * d <= temp_n:
        if temp_n % d == 0:
            factors.add(d)
            while temp_n % d == 0:
                temp_n //= d
        d += 1
    if temp_n > 1:
        factors.add(temp_n)
    return list(factors)

def find_primitive_root(p):
    if p == 2:
        return 1
    p_minus_1 = p - 1
    prime_factors_p_minus_1 = get_prime_factors(p_minus_1)

    for g in range(2, p):
        if is_primitive_root(g, p, prime_factors_p_minus_1):
            return g
    return None 

def power(a, b, m):
    res = 1
    a %= m
    while b > 0:
        if b % 2 == 1:
            res = (res * a) % m
        a = (a * a) % m
        b //= 2
    return res

def modInverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

# --- ElGamal 参数 ---
p = 2357
print(f"选择的素数 p = {p}")


alpha = find_primitive_root(p)
if alpha is None:
    print(f"未能找到模 {p} 的本原元。请检查素数 p。")
    exit()
print(f"找到的本原元 α = {alpha}")


a = random.randint(2, p - 2)
print(f"选择的私钥 a = {a}")

beta = power(alpha, a, p)
print(f"计算得到的公钥 β = {beta}")
print(f"公钥: (p={p}, α={alpha}, β={beta})")
print(f"私钥: a={a}")

print("-" * 30)

m = random.randint(0, p - 1)
print(f"选择的随机消息 m = {m}")

r = random.randint(2, p - 2)
print(f"选择的随机数 r = {r}")


c1 = power(alpha, r, p)

c2 = (m * power(beta, r, p)) % p
print(f"计算得到的密文 (c1, c2) = ({c1}, {c2})")

print("-" * 30)


s = power(c1, a, p)

s_inv = modInverse(s, p)

m_prime = (c2 * s_inv) % p
print(f"解密计算得到的 s = c1^a mod p = {s}")
print(f"解密计算得到的 s 的逆元 s_inv = {s_inv}")
print(f"解密得到的明文 m' = {m_prime}")


if m == m_prime:
    print("解密成功，明文 m' 与原始消息 m 一致。")
else:
    print("解密失败，明文 m' 与原始消息 m 不一致。")