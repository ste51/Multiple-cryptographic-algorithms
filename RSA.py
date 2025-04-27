import random
import base64
from math import sqrt


class RSA():
    def __init__(self,text,key,n):
        self.key = key
        self.text = text
        self.n = n

    def Encrypt(self):
        plaintext = self.text
        e = self.key
        n = self.n
        ciphertext = ''
        for i in plaintext:
            cipherchar = "%012d" % DieRepeat(e, n, 1, ord(i)) #整数赋值后变成
            ciphertext += cipherchar
            # ciphertext += chr(cipherchar)
        ciphertext = self.Base64word(ciphertext,'1')
        return ciphertext

    def Decrypt(self):
        orginciphertext = self.text
        orginciphertext = self.Base64word(orginciphertext, '0')
        ciphertext = []
        for j in range(0,len(orginciphertext),12):
            ciphertext.append(orginciphertext[j:j+12])
        d = self.key
        n = self.n
        plaintext = ''
        for i in ciphertext:
            plainchar = self.SquareBy(d,d,n,1,int(i),0)
            plaintext += chr(plainchar)
        return plaintext

    def Base64word(self,word, flag):
        if (flag == '1'):
            return str(base64.b64encode(word.encode()), 'utf-8')
        else:
            return str(base64.b64decode(word), 'utf-8')

    #平方乘 参数 n和n1都是一样的值,只是n后面会变，m是mod m，b是1,a是要加密的数字，count是根据位数循环的次数
    def SquareBy(self,n,n1,m,b,a,count):
        nlength = len(bin(n1))
        high = int('1' + '0' * (nlength - 3), 2)  # 取最高位
        j = int('1' * (nlength - 2), 2)
        if(n & high == high):
            b *= b * a
        else:
            b *= b
        b = b % m
        if(count == nlength-3): #之所以不使用n & j == 0,是因为存在一些数字后几位全为0的情况
            return b
        count += 1
        return self.SquareBy((n<<1)&j,n1,m,b,a,count) #(n<<1)&j保证二进制位数不变的，count根据二进制位数进行循环

#模重复平方算法 参数：n是幂，m是mod m,b是最后的结果，初始为1,a是要加密的数字
def DieRepeat(n,m,b,a):
    if(n & 0x1 == 1):
        b *= a
        b = b % m
    a *= a
    a = a % m
    if(n & 0xffff == 0):
        return b
    return DieRepeat(n>>1,m,b,a) #这里调用本身函数不用在参数中添加self,在外面添加self

#1000以内素数检验
def is_prime(n):
    primenumber = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    if n == 1:
        return 1 #表示n为素数
    # for i in range(2, int(sqrt(n))+1): #加入这个检测完所有数字
    b = sqrt(n) #提高运行速度,检测到n的根号就晓得是不是素数了
    for i in primenumber:#用1000以内的数字检验
        if i >= b:
            break
        elif n % i == 0:
            return 0 #表示n不为素数
    return 1


def Mod2(n):
    count = 0
    while(1):
        if(n % 2== 0):
            count += 1
        else:
            return count,n
        n = n//2

#米勒素数检测 n表示一个数字，time表示循环次数
def Miller_Rabin(n,time):
    a = [] #用来装每次得到的结果
    s,t = Mod2(n-1) #实现的n-1 = 2^s*t
    while(time): #实现b^t
        time -= 1
        k = random.randint(2, n-2)#范围就是2~n-2,其中包括2和n-2
        b = DieRepeat(t,n,1,k) #模重复平方
        if(b+1 == 0 or b-1 == 0):
            a.append(1)
            continue
        flag = 0
        orginpower = 0 #为了，b不用每次都重头开始计算，加快速度
        for i in range(0,s):
            power = 2 << i #向右移等于乘2
            k = b #k是b^t的结果
            b = DieRepeat(power-orginpower,n,1,k) #模重复平方
            orginpower = power #这个是为了让b不用每次都从1开始乘起来
            if(b + 1 == n or b == 1): #还不清楚为什么非要加b == 1才能使数字为素数，书上没有这样写，但是不加这个又确实大概率无法得到素数
                a.append(1)
                flag = 1
                break
        if(flag == 1):
            continue
        elif(flag == 0):
            a.append(0)
            continue
    if (0 in a):
        return 0 #返回0表示不是素数
    else:
        return 1 #返回1表示是素数

#把1000以内的素数检测和Miller_Rabin组合在一起
def DeterminePrime(n):
    if (is_prime(n) == 1):
        if (Miller_Rabin(n, 5) == 1): #进行5次米勒素数检验
            return 1 #n是素数
        else:
            return 0 #n不是素数
    else:
        return 0 #n不是素数

#找到为奇数的随机数
def RandomNumber(flag):
    while(1):
        if(flag == 1):
            number = random.randint(2**21,2**22)
        elif(flag == 0):
            number = random.randint(2**16,2**17)
        if(number & 0x1 == 0):#直接抛弃偶数，只使用奇数【为了提高效率】
            continue
        else:
            break
    return number

#生成p和q
def CreatepAndq():
    flag = 0
    while(1):
        if (flag == 0):
            p = RandomNumber(1)
            if(DeterminePrime(p) == 0):
                continue
            else:
                flag = 1
        q = RandomNumber(0)
        if(DeterminePrime(q) == 0 or p == q):
            continue
        else:
            return p, q

#辗转相除法,求d
def gcd(PhiN,e):
    a = [PhiN] #存储公因式化简每一次的过程
    while (e != 0):
        r = e
        a.append(r)  # 将计算过程中的值存起来
        e = PhiN % e
        PhiN = r
    m_n = 1
    d = 0
    for i in range(len(a)-2,-1,-1):
        d = (1-a[i]*m_n)//a[i+1] #进行转换
        m_n = d
    return d

text = input('请输入字符串：') #仅能输入数字和字母，不建议使用中文，因为没做处理
key = int(input('请输入(加密(e)/解密(d))密钥：')) #这里的e不宜太大，最好别超过100
n = int(input('请输入n(没有,则输入0)：'))
flag = int(input('加密输入1,解密输入0：'))
if(flag == 1):
    e = key
    if(n == 0):
        while(1):
            p, q = CreatepAndq()
            n = p * q
            PhiN = (p - 1) * (q - 1)
            d = gcd(PhiN,e)
            if(d < 0):
                continue
            else:
                break
        print('p和q', p, q)
        print('加密的密钥:d和n:',d,n)
    rsa = RSA(text,e,n)
    print(rsa.Encrypt())
else:
    d = key
    rsa = RSA(text,d,n)
    print(rsa.Decrypt())