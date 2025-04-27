#填充为512的倍数
def PadMessage(text):
    filltext = ''
    for i in text:
        filltext += '{0:08b}'.format(ord(i))
    orginfilllength = len(filltext)
    filltext += '1'
    while (len(filltext) % 512 != 448): #实现的就是512*n+448
        filltext += '0'
    filltext += bin(orginfilllength)[2:].zfill(64)
    return filltext

#循环左移
def CircularleftShift(bits,word):
    return ((word << bits) & 0xFFFFFFFF) | (word >> (32-(bits)))

#生成W
def SHADataExtend(M):
    W = []
    for j in range(0,len(M),32):
        W.append(int(M[j:j+32],2))
    for t in range(16,80):
        W.append(CircularleftShift(1,W[t-3]^W[t-8]^W[t-14]^W[t-16]))
    return W

def Compression(W,H):
    K = [0x5A827999,0x6ED9EBA1,0x8F1BBCDC,0xCA62C1D6]
    A = H[0]
    B = H[1]
    C = H[2]
    D = H[3]
    E = H[4]
    for t in range(80):
        if(t <= 19):
            f = (B & C) | (~B & D)
            Ki = K[0]
        elif(20<=t<=39):
            f = B^C^D
            Ki = K[1]
        elif(40<=t<=59):
            f = (B & C) | (B & D) | (C & D)
            Ki = K[2]
        else:
            f = B^C^D
            Ki = K[3]
        T = (CircularleftShift(5,A) + f + E + W[t] + Ki) & 0xffffffff
        E = D
        D = C
        C = CircularleftShift(30,B)
        B = A
        A = T
    H[0] = (A + H[0]) & 0xFFFFFFFF
    H[1] = (B + H[1]) & 0xFFFFFFFF
    H[2] = (C + H[2]) & 0xFFFFFFFF
    H[3] = (D + H[3]) & 0xFFFFFFFF
    H[4] = (E + H[4]) & 0xFFFFFFFF
    return H

text = 'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq'
padding = PadMessage(text)
H = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
for i in range(0,len(padding),512):
    W = SHADataExtend(padding[i:i+512])
    H = Compression(W, H)
print('%08x%08x%08x%08x%08x'%(H[0],H[1],H[2],H[3],H[4]))