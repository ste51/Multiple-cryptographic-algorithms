import copy
import re

class AES():
    def __init__(self,text,key):
        self.text = text  # 即可以是明文，也可以是密文
        self.allk = []
        key = self.convert0x_45(key) #转成列优先
        key1 = copy.deepcopy(key)
        for round in range(10):
            subkey = self.SubKey_45(key1, round)
            key1 = subkey


    def Encryption(self):
        plaintext = self.convert0x_45(self.text)
        # 全部转为列优先
        ciphertext = self.AddRoundKey_45(plaintext, self.allk[0:4], '1')
        for round in range(10):
            subbyte = self.SubBytes_45(ciphertext)  # S盒替换
            subbyte = self.OnemuTwo_45(subbyte, '1')  # 从列优先变成行优先
            shiftrow = self.ShiftRows_45(subbyte)
            if (round < 9):
                mixcolumn = self.MixColumns_45(shiftrow)  # 列混合
                mixcolumn = self.OnemuTwo_45(mixcolumn, '1')  # 从行优先再变为列优先
            else:
                mixcolumn = self.OnemuTwo_45(shiftrow, '1')
            subkey = self.allk[round * 4 + 4:round * 4 + 8]  # allk的前4行是列优先，解密时需要进行转换
            ciphertext = self.AddRoundKey_45(mixcolumn, subkey, '2')
        return ciphertext


    def Decryption(self):
        ciphertext = self.convert0x_45(self.text)
        # print('ciphertext is',ciphertext)
        # print('Encryption 中key', self.allk[0:4])
        #self.allk = [self.allk[i-4:i] for i in range(len(self.allk), 0, -4)]
        ki = []
        for i in range(len(self.allk), 0, -4):
            ki += self.allk[i - 4:i]
        self.allk = ki
        # print('Encryption 中key', self.printlist(self.allk[0:4]))
        # 全部转为列优先
        plaintext = self.AddRoundKey_45(ciphertext, self.allk[0:4], '1')
        # print('plaintext is',self.printlist(plaintext))
        for round in range(10):
            plaintext = self.OnemuTwo_45(plaintext, '1')  # 从列优先变成行优先
            # print('变行优先：plaintext1 is', self.printlist(plaintext))
            Invshiftrow = self.ShiftRows_45(plaintext,'-1')
            subbyte = self.SubBytes_45(Invshiftrow,'-1')  # S盒替换 #这里未做变换
            subbyte = self.OnemuTwo_45(subbyte,'1') #从行优先变成列优先
            subkey = self.allk[round * 4 + 4:round * 4 + 8]  # allk的前4行是列优先，解密时需要进行转换
            roundkey = self.AddRoundKey_45(subbyte, subkey, '2')
            if (round < 9):
                mixcolumn = self.OnemuTwo_45(roundkey, '1') #从列优先变成行优先
                plaintext = self.MixColumns_45(mixcolumn,'-1')  # 列混合
                plaintext = self.OnemuTwo_45(plaintext, '1')  # 从行优先再变为列优先
            else:
                plaintext = roundkey
        return plaintext

    def printlist(self,word):
        for i in word:
            print(i)
    def OnemuTwo_45(self,array_45,flag_45=''): #做列优先
        sumlist = []
        if(flag_45 == '1'): #列优先变成行优先
            sumlist = [[0] * 4 for i in range(4)]
            for i in range(4):
                for j in range(4):
                    sumlist[i][j] = array_45[j][i]
        else:
            for i in range(0, len(array_45), 4):  # 分组，相对于上面的简单
                sumlist.append(array_45[i:i + 4])
        return sumlist


    #字节替换
    def SubBytes_45(self,word_45,flag = ''):
        S = (0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
         0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
         0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
         0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
         0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
         0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
         0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
         0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
         0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
         0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
         0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
         0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
         0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
         0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
         0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
         0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16)
        if(flag == '-1'):
            S = (0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,)
        sum = []
        flag1 = 0
        for i in word_45:
            try: #try在这是用来判断是一维数组还是二维数组的
                for j in i:
                    if(len(j) == 1): #发现不是二维数组，主动抛出异常，就会被丢弃，不再执行try里面的代码
                        raise Exception
                    a = int(j, 16)
                    b = (a >> 4) * 16
                    d = a & 0x0f
                    sum.append(hex(S[b + d]))
            except:
                a = int(i, 16)
                b = (a >> 4) * 16
                d = a & 0x0f
                sum.append(hex(S[b + d]))
            else: #没抛出异常时，执行这一段
                flag1 = 1
        if(flag1 == 1):
            sum = self.OnemuTwo_45(sum)
        return sum

    #行位移
    def ShiftRows_45(self,word_45,flag = ''):
        C = [0,1,2,3]
        if(flag=='-1'):
            C=[-i for i in C]
        z = 0
        sum = []
        for j in word_45:
            sum.append(j[C[z]:]+j[:C[z]])
            z += 1
        return sum

    # 有限域上的乘法 GF(2^8)
    def GFMul(self, a, b):#这一段即可以用于加密，也可以用于解密
        p, hi_bit_set = 0, 0
        for counter in range(8):
            # print('---------------------第',counter,'次------------------')
            # print('b每一次的二进制:',bin(b),b)
            # print('a每一次的二进制:', bin(a),a)
            # print('b & 1:',b&1)
            if b & 1 != 0:  # 这里有个作用，当二进制循环时，为1则进入
                p ^= a  # 这个地方当最高位为1时，固定矩阵无论为0x2，还是0x3都是在最后异或1b，需要注意的是：0x3那种分成0x2·0xa^0x1·0xa这种，多出来的异或本身【0x1·0xa】是被放到了异或里面，加起来刚好就是本身
#这里相当于执行的是 b<<n+b<<n-1+...+b<<1,异或相当于加
                # print('p ^= a:',bin(p),p)
            # print('b1 is',b)
            hi_bit_set = a & 0x80  # 这里的最高位主要是用于异或1b
            # print('hi_bit_set：',hi_bit_set)
            a = (a << 1) & 0xff  # 这里把下面b除去的，乘回来,并且'& 0xff'对0x2和0x3的影响很大，0x2右移到10000000时，变为经过a^1b就
            # print('a << 1:',bin(a))
            if hi_bit_set != 0:
                a ^= 0x1b  # x^8 + x^4 + x^3 + x + 1，是代表这个意思，但是为什么不是9b,而是1b?这是因为在异或1b之前，a先进行了右移1位变成了00000000，0和1异或为1
# 右移是方便执行之后的程序，但是在这就会出问题，本来该是10000000^9b,但是异或相同为0,相异为1，那么a最高为没有1，那9b也最高位也不能有1，就变成了1b
                # print('a^1b :',bin(a))
            b >>= 1  # 这里相当于b除以2
            # print('b >> 1 :',bin(b))
        # print('p & 0xff: ',p & 0xff)
        # exit()
        return p & 0xff

    def MixColumns_45(self, word, flag=''):
        Fixedmatrix = [0x2, 0x3, 0x1, 0x1]
        if (flag == '-1'):
            Fixedmatrix = [0xE, 0xB, 0xD, 0x9]
        temp = []
        sum = []
        p = 0
        for k in range(len(Fixedmatrix)):
            temp = []
            for i in range(len(Fixedmatrix)):
                p = 0
                for j in range(len(word[0])):
                    a = self.GFMul(Fixedmatrix[j], int(word[j][i], 16))
                    p ^= a
                temp.append(hex(p))
            sum.append(temp)
            Fixedmatrix = self.RotByte_45(Fixedmatrix, -1)
        return sum

    #轮密钥加
    def AddRoundKey_45(self,word_45,key_45,flag_45=''):
        if(flag_45 == '1'): #为了把一维的转成二维:列优先
            word_45 = self.OnemuTwo_45(word_45)
        # print('ciphertext1 is', self.printlist(word_45))
        # print('word_45 is',word_45)
        # print('key_45 is',key_45)
        sum = []
        for i in range(len(word_45)):
            for j in range(len(word_45[0])):
                # print('key和word',key_45[i][j],word_45[i][j])
                sum.append(hex(int(key_45[i][j],16)^int(word_45[i][j],16)))
        sum=self.OnemuTwo_45(sum)
        return sum

    #子密钥进行位移
    def RotByte_45(self,word_45,k):
        return word_45[k:]+word_45[:k]

    #Rcon的生成
    def RCON_45(self,round_45):
        RC = ['0x01', '0x02', '0x04', '0x08', '0x10', '0x20', '0x40', '0x80', '0x1B', '0x36']
        sum = []
        sum.append(RC[round_45])
        sum += ['0x00','0x00','0x00']
        return sum

    def SubKey_45(self,word_45,round_45): #前面的都是一行一行的存，这里一列一列来存 #这里可能出现问题 subbytes函数进行了更换
        k = []
        temp = []
        if(round_45 == 0):
            for i in range(0,len(word_45),4): #分组
                k.append(word_45[i:i+4])
            self.allk = copy.deepcopy(k)
        else:
            k = word_45
        Rcon = self.RCON_45(round_45)
        k3change = self.SubBytes_45(self.RotByte_45(k[-1],1))# 该步将最后一列进行了位移，S盒变换
        for i in range(len(k[0])):  # k0和k3和Rcon异或得到k4
            temp.append(hex(int(k[0][i],16) ^ int(k3change[i],16) ^ int(Rcon[i],16)))
        k.append(temp)
        for j in range(1,4): #得到k5
            temp = []
            for i in range(len(k[0])): #k0和k4和Rcon异或
                temp.append(hex(int(k[j][i],16)^int(k[j+3][i],16)))
            k.append(temp)
        subkey = k[4:8] #这个是以列优先的
        self.allk += subkey
        return subkey

    def convert0x_45(self,word_45):
        return ['0x'+str(v) for v in word_45]

# def WordmuHex(word,flag):
#     if flag == 0: #中英混合字符转hex
#         return word.encode().hex()
#     else: #hex转字符
#         m = re.search(r'[0]+$',word)
#         if(m != None):
#             word = word[:m.start()]
#         else:
#             word = word
#         return bytes.fromhex(word).decode()
#
# def list2char(word):
#     sum = ''
#     for i in word:
#         for j in i:
#             sum += j.replace('0x','').zfill(0)
#     return sum
#plaintext1 = ['19', '3d', 'e3', 'be', 'a0', 'f4', 'e2', '2b', '9a', 'c6', '8d', '2a', '9a', 'c6', '8d', '2a', 'e9', 'f8', '48', '08']
# plaintext = ['80', '5E', '6A', '36', '53', '25', '3A', '66', '63', '35', '69', '03', '20', '6C', '28', '06']
plaintext =  ['19', '3d', 'e3', 'be', 'a0', 'f4', 'e2', '2b', '9a', 'c6', '8d', '2a', '9a', 'c6', '8d', '2a']
# ciphertext = ['22', '1a', 'b3', '07', 'e1', '07', '8c', '09', '19', '64', 'e2', '27', '9c', '8d', 'f3', '24']
ciphertext = ['8', 'f0', '7', 'c8', '5c', '80', 'fe', '21', 'da', 'e6', 'cc', '18', '8c', '48', '91', 'f9']
key = ['a0','fa','fe','17','88','54','2c','b1','23','a3','39','39','2a','6c','76','05']
print('明文是',plaintext)
x = AES(plaintext,key)
print('最后的密文为：',x.Encryption())
print('密文是',ciphertext)
y = AES(ciphertext,key)
print('最后的解密为：',y.Decryption())
# # plaintext = ['32','43','f6','a8','88','5a','30','8d','31','31','98','a2','e0','37','07','34']
#key = ['a0','fa','fe','17','88','54','2c','b1','23','a3','39','39','2a','6c','76','05']
#key = ['75', '35', '6B', '99', '05', '61', '39', '56', '73', '62', '05', '31', '00', '55', '09', '32']
# word = input('请输入文字:')
# word = re.findall(r'.{2}',WordmuHex(word,0))
# word = re.findall(r'.{2}','ebd40c8e082c6d655d360895842bc4d')
# flag = input('是加密(1)还是解密(0):')
# key = input('请输入密钥:')
# key = re.findall(r'.{2}',WordmuHex(key,0)[:32])
# print('key is',key)
# if(len(key) != 16):
#     key += ['00'] * (16 - len(key))
# for i in range(0,len(word),16):
#     text = word[i:i+16]
#     print('text is',text)
#     if (len(text) != 16):
#         text += ['00'] * (16 - len(text))  # 使其为16个
#     if(flag == '1'):
#         x = AES(text,key)
#         a = x.Encryption()
#         print('最后的密钥为：',list2char(a))
#     elif(flag == '0'):
#         x = AES(text, key)
#         a = x.Decryption()
#         print(a)
#         print('解密：', WordmuHex(list2char(a),1))
# ciphertext = ['8', 'f0', '7', 'c8', '5c', '80', 'fe', '21', 'da', 'e6', 'cc', '18', '8c', '48', '91', 'f9']