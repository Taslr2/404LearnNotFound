# import random
#
# p=613
# q=827
# n=506951
# x=0
# # 计算勒让德符号
# def legendre_symbol(a, p):
#     a=a%p
#     if a==1: return 1
#     elif a==0: return 0
#     elif a==-1: return -1
#     elif a==2: return pow(-1,(p**2-1)//8)
#     else: return pow(-1,(a-1)*(p-1)//4)* legendre_symbol(p%a, a)#递归计算防止溢出
#
# # 计算最大公因数
# def gcd(a,b):
#     if a<b:
#         temp=b
#         b=a
#         a=temp
#
#     if a%b==0:
#         return b
#     else:
#         a = a % b
#         return gcd(a,b)
# # 计算c
# def calculate_c_value(x,y,m,n):
#     y=y**2%n
#     if m==0:
#         return y
#     else:
#         y=y*x%n
#         return calculate_c_value(x,y,m-1,n) #递归计算防止溢出
#
# m=int(input("请输入要加密的消息："))
# #计算x的值
# for i in range(0,n-1):
#     if legendre_symbol(i,p) ==-1 and legendre_symbol(i,q)==-1:
#         x=i
#         print("x的值为:",x)
#         break
# #取y
# while True:
#     y = random.randint(1, n-1)
#     if gcd(y,n) ==1:
#         print("y的值为：",y)
#         break
# #计算c的值
# c=calculate_c_value(x,y,m,n)
# print("c的值为：",c)
#
# # 计算cp，cq
# cp=legendre_symbol(c,p)
# cq=legendre_symbol(c,q)
# print("c/p的值为：",cp)
# print("c/p的值为：",cq)
#
# # 输出m'
# if cp==cq==1:
#    m_1=0
# else:
#     m_1=1
# print("m\'的值为：",m_1)
print((2**279)%1117)