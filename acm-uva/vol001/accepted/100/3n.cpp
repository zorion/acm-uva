#include <iostream>

int alg(int n){
	int i=1;
	while (n>1){
		if (n%2 == 0){
			n = n/2;
		}else{
			n = 3*n + 1;
		}
		++i;
	}
	return i;
}

int max_cycles(int i, int j){
	int iAux,iMax;
	if (j<i){
		iAux=j;
		j=i;
		i=iAux;
	}
	iMax = alg(j);
	for(iAux=i;iAux<j;++iAux){
		int iResult = alg(iAux);
		if (iResult>iMax)
			iMax=iResult;
	}
	return iMax;
}

int main(){
	int i, j;
	while(std::cin>>i>>j){
		std::cout<<i<<" "<<j<<" "<<max_cycles(i,j)<<std::endl;
	}
}

