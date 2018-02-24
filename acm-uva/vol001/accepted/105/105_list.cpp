#include <iostream>
#include <list>

#define LOW 0
#define TOP 1
#define END 2

class SB {
public:
	int pos, height;
	void print(void){
		std::cout << pos << " " << height;
	}
};

class Skyline{
public:
	std::list<SB> data;

	void print(void) {
		std::list<SB>::iterator it;
		it=data.begin();
		it->print();
		for (++it; it != data.end(); ++it) {
			std::cout<< " ";
			it->print();
		}
		std::cout << std::endl;
	}

	void insert(std::list<SB>::iterator it, SB s){
		data.insert(it, s);
	}

	std::list<SB>::iterator remove(std::list<SB>::iterator it){
		return data.erase(it);
	}

	
	void insert_building(int a, int h, int b) {
		// States:
		//		before
		//		
		std::list<SB>::iterator it;
		SB new_item;
		new_item.pos = a;
		new_item.height = h;

		bool new_is_bigger, follow_the_flow;
		int last_height;
		new_is_bigger = true;
		follow_the_flow = false;
		last_height = 0;

		if (h==0 || b <= a)
			return;

		it = data.begin();
		// go to the start of the new_building and check if it is greater
		//POST: 
		//    *it is the first item that it->pos >= a or the end of the list
		//    new_is_bigger if the last collected building is lower
		//    last_height is the previous level
		while(it!=data.end() && it->pos < a){
			last_height = it->height;
			++it;
		}

		if(it == data.end()) {
			follow_the_flow = true;
			if (last_height != h) {
				insert(it, new_item);
				last_height = h;
			}
		}else if (it->pos > a) {
			if (last_height < h) {
				follow_the_flow = true;
				insert(it, new_item);
			}
		} else { // it->pos == a, not ending
			if (last_height == h && it -> height < h) {
				follow_the_flow = true;
				it = remove(it);
			} else {
				last_height = it->height;
				new_is_bigger = last_height < h;
				it->height = new_is_bigger?h:last_height;
				follow_the_flow = new_is_bigger;
				++it;
			}

		}
		// std::cout << "   first sdg adga  "<< last_height << " \n";
		
		//Now decide for each "old" top-left if it stays, changes or it is removed
		//POST:
		//     *it is the first item that it->pos >= b or the end of the list
		//     follow_the_flow if our new building was the last active
		while(it!=data.end() && it->pos < b){
			int prev_height = last_height;
			last_height = it -> height;
			if (last_height <= h) {
				if (!follow_the_flow  && prev_height != h){
					new_item.pos = it->pos;
					new_item.height = h;
					insert(it, new_item);
				}
				it = remove(it);
				follow_the_flow = true;
			}else{
				follow_the_flow = false;
				++it;
			}
		}
		

		if (it == data.end()){
			new_item.pos = b;
			new_item.height = 0;
			insert(it, new_item);
		} else if (follow_the_flow && h != last_height && it->pos != b) {
			new_item.pos = b;
			new_item.height = last_height;
			insert(it, new_item);
		} 
	}

};


int main() {
	int a, h, b;
	Skyline s;
	while(std::cin >> a >> h >> b) {
		s.insert_building(a, h, b);
	}

	s.print();
}