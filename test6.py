#E盒扩展+k密钥+S盒+P盒+异或
import test6
import re
import base64


def Ascii2Bin(word):
    sum = ''
    for i in word:
        sum += bin(ord(i)).replace("0b", "").zfill(16)
    if(len(sum) != 64):
        sum = sum.ljust(64,'0')
    return sum


def Printbin(word,flag):
    if(flag == 1):
        printword = ''
        test = re.findall(r'.{16}',word)
        for i in test:
            printword += chr(int(i, 2))
        return printword
    else:
        printword = ''
        for i in re.findall(r'.{16}', word):
            a = chr(int(i, 2))
            if (a != chr(0)):  # 除去最后填充的元素
                printword += a
        return printword


def Base64word(word,flag):
    if(flag == 1):
        return str(base64.b64encode(word.encode()),'utf-8')
    else:
        return str(base64.b64decode(word),'utf-8')


word = input("输入字符串：")
key = input("请输入8个数字的密钥：")
judge = input("加密输入1,解密输入0：")


k = test6.CreateK(key)  # 创造k密钥的实例
Kword = k.createKword()  # 得到Kword的密钥
if(judge == '0'):
    Kword = Kword[::-1]
    word = Base64word(word, 2)
finalword  = ''
finalword2 = ''
step = 4
for i in range(0, len(word), step):#对输入的字符串分组，4个为一组;
    a = word[i:i + step]
    BinWord = Ascii2Bin(a)
    Ipword = test6.IP(BinWord)
    L = Ipword[:32]
    R = Ipword[32:]
    for j in range(16):
        Eword = test6.extendE(R)  # E盒扩展后，再把列表变成字符串
        SP = test6.SboxaddPbox(bin(int(Eword, 2) ^ int(Kword[j], 2)))  # S盒和P盒的置换
        Rbin = bin(int(L, 2) ^ int(SP.SboxaddPbox1(), 2)).replace("0b", "").zfill(32)  # L和P盒置换后的异或,并替换0b
        L = R  # Li = Ri-1
        R = Rbin  # 这两步同样是16轮完后的左右交换
    (L,R) = (R,L)
    clearlist = L + R  # 16轮后的L和R合并
    Ipreword = test6.IPreverse(clearlist)
    printword = Printbin(Ipreword,1)
    finalword += printword
    if(judge == '1'):
        finalword2 += Base64word(printword,1)


if(judge == '1'):
    print("加密密文：",finalword2)
else:
    print("解密明文：",finalword)