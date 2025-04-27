#该程序编写出来后的缺点:只能输入英文【不能输入数字和中文】；不区分大小写；2^32-1实在太大，加载速度十分慢；
#半成品吧。。。大部分明文能加密和解密，但存在少部分不行，主要是不想编了。。。。
#a-z和A-Z全部变成0-25
def LetterLowerCase(key):
    M = []
    for i in key:
        if (i >= 'A' and i <= 'Z'):
            i = ord(i) - 65
        elif (i >= 'a' and i <= 'z'):
            i = ord(i) - 97
        elif (i == ' '):
             i = 26
        M.append(i)
    return M

#数字变成大写的A-Z
def Number2Word(word):
    string = ''
    for i in word:
        if(i < 26):
            string += chr(i+65) #全部变成大写
        else:
            string += ' '
    return string

#n为LFSR生成(2^8-1)位orginkey
def LFSR(key):
    listkey = LetterLowerCase(key)
    orginkey = ''
    for i in listkey:
        orginkey += bin(i)[2:].zfill(8)
    print(orginkey)
    input = ''
    for i in range(pow(2,8)-1): #pow(2,n)-1实现2^n-1,n=32要运行很久【暂未找到公式简化运行过程】
        bina = int(orginkey,2)
        #注意底下可以通过一个for循环来实现f(a1,a2,...,an)=cna1 ^ c(n-1)a1 ^...^clan 【其中cn规定必须为1】 由于懒，不想写了
        a1 = bina & 0x1 #获取第一位
        a5 = (bina & 0x10)>>4 #获取第4位
        a9 = (bina & 0x100)>>8 #获取第9位
        a13 = (bina & 0x1000)>>12 #获取第13位
        bina = bina >> 1
        bina = bina & 0x7FFFFFFF
        input += str(a1) #输出的密钥
        orginkey = str(a1^a5^a9^a13) + bin(bina)[2:].zfill(31) #替换从左到右的第一位
    return input

word = input('字符串：')
key = input('加/解密密钥：')
flag = input('加密输入0,解密输入1：')
lowerword = LetterLowerCase(word)
keyname = LFSR(key)
print('lowerword is',lowerword)
print('keyname is',keyname)
if(flag == '1'):
    j = 0
    Y = []
    for i in lowerword:
        t = (i+int(keyname[j:j+8],2)) % 27 #之所以是27是因为要包含空格，不算空格的话，就是26
        Y.append(t)
        j += 8
    print(Number2Word(Y))
else:
    j = 0
    M = []
    for i in lowerword:
        t = (i - int(keyname[j:j + 8], 2)) % 27  # 之所以是27是因为要包含空格，不算空格的话，就是26
        M.append(t)
        j += 8
    print(Number2Word(M))