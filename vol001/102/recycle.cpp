#include<iostream>
#include<string>
#define C_B 0
#define C_G 1
#define C_C 2

int cost(int viSrc[][3],int i1,int i2, int i3){
return viSrc[0][(1+i1)%3]+viSrc[0][(2+i1)%3] +viSrc[1][(1+i2)%3]+viSrc[1][(2+i2)%3] +viSrc[2][(1+i3)%3]+viSrc[2][(2+i3)%3];
}

void solve(int viSrc[][3]){
	int iMinCost, iAux;
	std::string szPermut;
	iMinCost = cost(viSrc,C_B,C_C,C_G);
	szPermut = "BCG";

	iAux = cost(viSrc,C_B,C_G,C_C);
	if(iAux<iMinCost){
		szPermut="BGC";
		iMinCost=iAux;
	}

	iAux = cost(viSrc,C_C,C_B,C_G);
	if(iAux<iMinCost){
		szPermut="CBG";
		iMinCost=iAux;
	}

	iAux = cost(viSrc,C_C,C_G,C_B);
	if(iAux<iMinCost){
		szPermut="CGB";
		iMinCost=iAux;
	}
	iAux = cost(viSrc,C_G,C_B,C_C);
	if(iAux<iMinCost){
		szPermut="GBC";
		iMinCost=iAux;
	}
	iAux = cost(viSrc,C_G,C_C,C_B);
	if(iAux<iMinCost){
		szPermut="GCB";
		iMinCost=iAux;
	}
	std::cout<<szPermut<<" "<<iMinCost<<std::endl;
}

int main(){
	int iAux,i,j;
	int viBin[3][3];
	i=j=0;
	while(std::cin>>iAux){
		viBin[i][j]=iAux;
		if(++j==3){
			j=0;
			if(++i==3){
				i=0;
				solve(viBin);
			}
		}
	}
}
