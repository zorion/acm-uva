#include<iostream>
using namespace std;

//2,3,2*2,5,2*3,3*3,

bool isUgly(long number)
{
     long last;
     while(number>1){
                last=number;
                if(number%2==0)number=number/2;
                if(number%3==0)number=number/3;
                if(number%5==0)number=number/5;
                if(last==number)return false;
                }
     return true;
 }
int main(){
    long number;
    int iUglies;

    number=0;
    iUglies=0;
    
    while(iUglies<=1500){
                   ++number;
                   if(isUgly(number)){
                               iUglies++;
                               cout<<iUglies<<": "<<number<<endl;
                               }
                   };
    return 0;
}
