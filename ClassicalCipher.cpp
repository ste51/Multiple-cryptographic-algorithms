// 古典密码
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
char a[20] = "RZfhrJhr##6opwG";
int main()
{
	char s[20];
	char b[20];
	int n,i,k,key,j,z;
	printf("Hello,this is a easyre\n");
	printf("please input the flag:");
	// 替换为安全的fgets输入
    if (!fgets(s, sizeof(s), stdin)) {
        printf("输入失败\n");
        return 1;
    }
	n = strlen(s);
	if(n != 15)
	{
		printf("error!");
		exit(0);
	}
	key = 3;
	for(i = 0;s[i]!='\0';i++)
	{
		s[i] += 3;
	}
	for(i = 0;s[i] !='\0';i++)
	{
		k = (i+key)%n;
		b[k] = s[i];
	}
	b[i]='\0';
	strcpy(s,b);
	k = 0;
	z = n/3;
	for(i = 0;s[i] != '\0';i+=3)
	{	
		k = i/3;
		for(j = 0;j<3;j++)
		{
			b[k+j*z]=s[i+j];
		}
	}
	b[i] = '\0';
	strcpy(s,b);
	if(strcmp(s,a) == 0)
	{
		printf("Congratulations!!!!!!!!!!!!!!!!!!\n");
	}
	else
	{
		printf("Try again\n");
	}
	return 0;
}