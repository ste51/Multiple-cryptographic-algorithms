// RC4加密算法
#include<stdio.h>
#include<string.h>
#include "base64.h"
void Swap(int* p, int* q)
{
        int tmp = *p;
        *p = *q;
        *q = tmp;
}

int* init_S(char* key)
{
        static int S[256]; //C 不支持在函数外返回局部变量的地址，除非定义局部变量为 static  变量
        for (int i = 0; i < 256; i++) {
               S[i] = i;
        }
        int j = 0;
        int temp = 0;
        for (int i = 0; i < 256; i++) {
               j = (j + S[i] + key[i % strlen(key)]) & 0xff;
               Swap(&S[i], &S[j]);
        }
        return S;
}

char* EnAndDe(char* word, int S[])
{
        int i = 0, j = 0;
        int k;
        static char text[1000];
        for (int z = 0; word[z] != '\0'; z++) {
               i = (i + 1) & 0xff;
               j = (j + S[i]) & 0xff;
               Swap(&S[i], &S[j]);
               k = word[z] ^ S[(S[i] + S[j]) & 0xff];
               text[z] = k;
        }
        return text;
}

int main()
{
        char word[] = "haode"; //这个是需要加密的字符串
        //char word[] = "nVgpFNE="; //需要解密的字符串
        char key[] = "abcdefg"; //密钥
        int flag = 1; //用于指示是加密还是解密:加密为1，解密为0
        char* word1;
        char* cipher;
        char* text;
        int* S;
        S = init_S(key); //接受函数返回的数组
        if (flag == 1) //加密
        {
               cipher = EnAndDe(word, S);
               text = base64_encode(cipher); //由于加密后的字符串不方便存储，就转换成base64【另一种解决方案：直接加密后得到数字，不使用字符串】
               printf("加密后字符串:%s\n", text);
        }
        else if (flag == 0) //解密
        {
               word1 = base64_decode(word);
               text = EnAndDe(word, S);
               printf("解密后的字符串：%s\n", text);
        }
}