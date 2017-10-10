#include<iostream>
#include<string>
#define C_EXIT  0
#define C_REMOVE 1
#define C_KEEP  2
#define C_ERROR 3
#define C_NULL -1
#define C_PRINT -2

void initBlock(int blocks[][3], int iBlock){
	blocks[iBlock][0]=iBlock;
	blocks[iBlock][1]=C_NULL;
	blocks[iBlock][2]=C_NULL;
}

void init(int b[][3],int n){
	int i;
	for(i=0;i<n;++i) initBlock(b,i);
}

int getStringOption(){
	std::string s;
	std::cin>>s;
	if(0==s.compare("quit")) return C_EXIT;
	else if(0==s.compare("print")) return C_PRINT;
	else if(0==s.compare("move") || 0==s.compare("onto")) return C_REMOVE;
	else if(0==s.compare("pile") || 0==s.compare("over")) return C_KEEP;
	return C_ERROR;
}


int getStack(int blocks[][3], int iBlock) {
	return blocks[iBlock][0];
}

int nextBlock(int blocks[][3], int iBlock){
	return blocks[iBlock][1];
}

int prevBlock(int blocks[][3], int iBlock){
	return blocks[iBlock][2];
}

void writeOutput(int blocks[][3],int n){
	int i,j;
	for(i=0;i<n;++i){
		std::cout<<(i)<<":";
		if(getStack(blocks,i)==i)
			std::cout<<" "<<(i);
		j=i;
		while(nextBlock(blocks,j)!=C_NULL){
			j=nextBlock(blocks,j);
			if(getStack(blocks,j)==i)
				std::cout<<" "<<(j);
		}
		std::cout<<std::endl;
	}
}
//move the block iSource and above to top of the stack where block iTarget is
void take(int blocks[][3], int  iSource, int iTarget){
	int iStackTarget = getStack(blocks,iTarget);
	int iAux;

	//previous block of the block to be moved is a new top block
	iAux=prevBlock(blocks,iSource);
	if(iAux!=C_NULL)
		blocks[iAux][1]=C_NULL;

	iAux=nextBlock(blocks,iTarget);

	while(iAux!=C_NULL){//find last block in stack
		iTarget=iAux;
		iAux=nextBlock(blocks,iAux);
	}
	//The block iSource is on top of iTarget, and it is in its stack
	blocks[iTarget][1]=iSource;
	blocks[iSource][2]=iTarget;
	blocks[iSource][0]=iStackTarget;

	iAux = nextBlock(blocks,iSource);
	while(iAux!=C_NULL){//set the stack for the rest of the pile over A
		blocks[iAux][0]=iStackTarget;
		iAux=nextBlock(blocks,iAux);
	}

}
void release(int blocks[][3], int iBlock){
	int iAux;

	iAux=nextBlock(blocks,iBlock);
	//now, iBlock is a top
	blocks[iBlock][1]=C_NULL;

	//Move the following blocks to their INITIAL position
	while(iAux!=C_NULL){
		iBlock=nextBlock(blocks,iAux);
		initBlock(blocks,iAux);//returns the block to the initial status
		iAux=iBlock;
	}

}

//PRE: iA and iB are not in the same stack
void simulate(int blocks[][3], int iA, int iOA, int iB, int iOB){
	int i;
	if(iOA==C_REMOVE)
		release(blocks,iA);
	if(iOB==C_REMOVE)
		release(blocks,iB);

	take(blocks,iA,iB);
}

void solve_problem(int n){
	int iOptionA, iOptionB;
	int iBlockA, iBlockB;
	int blocks[n][3];

	init(blocks,n);

	iOptionA = getStringOption();
	while(iOptionA!=C_EXIT){
		if(iOptionA==C_PRINT){
			writeOutput(blocks,n);
		}else{
			std::cin>>iBlockA;
			iOptionB = getStringOption();
			std::cin>>iBlockB;

			if(getStack(blocks,iBlockA)!=getStack(blocks,iBlockB))
				simulate(blocks,iBlockA,iOptionA,iBlockB, iOptionB);
		}
		iOptionA = getStringOption();
	}

	writeOutput(blocks,n);
}

int main(){
	int n;
	while(std::cin>>n)
		solve_problem(n);
}

