# RC4 python实现
import base64
#初始化
def init(key):
    S = []
    for i in range(256):
        S.append(i)
    j = 0
    for i in range(256):
        j = (j+S[i]+ord(key[i%len(key)]))%256
        S[i],S[j] = S[j],S[i]
    return S

#加密和解密
def EnAndDe(word,S):
    i = 0
    j = 0
    sum = ''
    for BYTE in word:
        i = (i+1)% 256
        j = (j+S[i]) % 256
        S[i],S[j] = S[j],S[i]
        k = ord(BYTE)^S[(S[i]+S[j])%256]
        sum += chr(k)
    return sum

def Base64word(word,flag):
    if(flag == '1'):
        return str(base64.b64encode(word.encode()),'utf-8')
    else:
        return str(base64.b64decode(word),'utf-8')

if __name__ == '__main__':
    word = input('请输入字符串:')
    key = input('请输入密钥:')
    flag = input('加密输入1，解密输入0:')
    S = init(key)
    if(flag == '1'):
        print(Base64word(EnAndDe(word,S),flag))
    else:
        word = Base64word(word,flag)
        print(EnAndDe(word,S))