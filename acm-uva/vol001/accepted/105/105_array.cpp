#include <iostream>
#include <list>
#define N 10000


class Skyline{
public:
	int left;
	int right;
	int V[N];

	void restart(){
		left=N;
		right=0;
		// for(int i=0; i < N; ++i) {
		// 	V[i] = 0;
		// }
	}
	void cleanup(int a, int b){
		for(int i=a; i < left; ++i) {
			V[i] = 0;
		}
		for(int i=right; i < b; ++i) {
			V[i] = 0;
		}
	}

	void print(void) {
		int it, last;
		if (left > right){
			return;
		}
		it=left;
		last = V[it];
		std::cout << it << ' ' << last;
		for (++it; it < right; ++it) {
			if(last != V[it]){
				last = V[it];
				std::cout<< ' ' << it << ' ' << V[it];
			}
		}
		std::cout << ' ' << right << ' ' << 0 << std::endl;
	}

	void insert_building(int a, int h, int b) {
		cleanup(a,b);
		left = std::min(a, left);
		right = std::max(b, right);
		for (int i=a; i<b; ++i){
			V[i] = std::max(V[i], h);
		}

	}

};


int main() {
	int a, h, b;
	Skyline s;
	s.restart();
	while(std::cin >> a >> h >> b) {
		s.insert_building(a, h, b);
		// std::cout << "insert (" << a << ", " << b << ") " << h << std::endl << "buildings: "; s.print();
	}

	s.print();
}