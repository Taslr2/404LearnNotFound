import random

def legendre_symbol(a, p):
    """计算勒让德符号 (a/p)"""
    if a == 0:
        return 0
    if a == 1:
        return 1
    if a % 2 == 0:
        return legendre_symbol(a // 2, p) * pow(-1, (p * p - 1) // 8)
    return legendre_symbol(p % a, a) * pow(-1, (a - 1) * (p - 1) // 4)

def mod_pow(base, exponent, modulus):
    """计算模幂"""
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent >>= 1
    return result

def solovay_strassen(n, t):
    """
    素性检验算法
    n: 待检验的数
    t: 测试轮数
    """
    if n == 2:
        return True, 0, "是素数"
    if n < 2 or n % 2 == 0:
        return False, 0, "是合数"

    for i in range(t):
        # (i) 随机选取小于n的正整数b
        b = random.randrange(2, n)
        print(f"\n第{i+1}轮测试:")
        print(f"随机选择的b = {b}")
        
        
        power = mod_pow(b, (n-1)//2, n)
        print(f"b^((n-1)/2) mod n = {power}")
        
        # (i) 第一步检查
        if power != 1 and power != n-1:
            return False, i+1, "(i) - 是合数"
            
    
        jacobi = legendre_symbol(b, n)
        print(f"(b/n) = {jacobi}")
        
        # (ii) 第二步检查
        if power % n != jacobi % n:
            return False, i+1, "(ii) - 是合数"
    
    # (iii) 如果通过了t轮测试
    return True, t, "(iii) - 可能是素数"

if __name__ == "__main__":
    n = 506951  
    t = 10     
    
    print(f"对n={n}进行Solovay-Strassen素性检验，测试轮数t={t}\n")
    
    is_probable_prime, rounds, position = solovay_strassen(n, t)
    
    print(f"\n测试结果：")
    print(f"总轮数: {rounds}")
    print(f"结束位置: {position}")
    if is_probable_prime:
        print(f"{n}可能是素数，出错概率不超过(1/2)^{t}")
    else:
        print(f"{n}是合数")
