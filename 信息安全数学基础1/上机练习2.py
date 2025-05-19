import random

# 快速幂算法
def power_mod(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

# 扩展欧几里得算法
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

# 求模逆元
def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('模逆元不存在')
    else:
        return x % m

# 判断一个数是否为素数
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# 计算欧拉函数φ(n)
def euler_phi(n):
    if n == 1:
        return 1
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

# 寻找本原元
def find_primitive_root(p):
    if not is_prime(p):
        raise ValueError(f"{p} 不是素数")
    
    # 计算φ(p-1)的所有不同素因子
    phi = p - 1
    factors = set()
    d = 2
    while d * d <= phi:
        while phi % d == 0:
            factors.add(d)
            phi //= d
        d += 1
    if phi > 1:
        factors.add(phi)
    
    # 检查2到p-1之间的每个数
    for g in range(2, p):
        is_primitive = True
        for factor in factors:
            # 检查g^((p-1)/factor) mod p是否等于1
            if power_mod(g, (p - 1) // factor, p) == 1:
                is_primitive = False
                break
        if is_primitive:
            return g
    
    return None  

def main():
    # ElGamal参数
    p = 2357  # 素数
    print(f"素数 p = {p}")
    
    # 寻找本原元
    alpha = find_primitive_root(p)
    print(f"找到的本原元 α = {alpha}")
    
    # 随机选择私钥 a ∈ Zp-1
    a = random.randint(2, p - 2)
    print(f"随机选择的私钥 a = {a}")
    
    # 计算公钥 β = α^a mod p
    beta = power_mod(alpha, a, p)
    print(f"公钥 β = α^a mod p = {alpha}^{a} mod {p} = {beta}")
    print(f"完整公钥 (p, α, β) = ({p}, {alpha}, {beta})")
    
    # 随机选择明文 m ∈ Zp
    m = random.randint(1, p - 1)
    print(f"\n随机选择的明文 m = {m}")
    
    # 随机选择 r ∈ Zp-1
    r = random.randint(2, p - 2)
    print(f"随机选择的加密随机数 r = {r}")
    
    # 加密
    c1 = power_mod(alpha, r, p)
    print(f"\n计算 c1 = α^r mod p = {alpha}^{r} mod {p} = {c1}")
    
    br = power_mod(beta, r, p)
    print(f"计算 β^r mod p = {beta}^{r} mod {p} = {br}")
    
    c2 = (m * br) % p
    print(f"计算 c2 = m·β^r mod p = {m}·{br} mod {p} = {c2}")
    
    print(f"最终密文 (c1, c2) = ({c1}, {c2})")
    
    # 解密
    s = power_mod(c1, a, p)
    print(f"\n计算 s = c1^a mod p = {c1}^{a} mod {p} = {s}")
    
    s_inverse = mod_inverse(s, p)
    print(f"计算 s的模逆元 s^(-1) mod p = {s_inverse}")
    
    m_prime = (c2 * s_inverse) % p
    print(f"计算 m' = c2 · s^(-1) mod p = {c2} · {s_inverse} mod {p} = {m_prime}")
    
    print(f"\n解密后的明文 m' = {m_prime}")
    print(f"验证: m == m' ? {'✓' if m == m_prime else '✗'}")

if __name__ == "__main__":
    main()