
#include<iostream>
#include<vector>

typedef std::vector<std::vector <int> > Graph;

bool fits(int* A, int* B, int num_cols){
    for(int i=0; i<num_cols; i++){
        if(A[i] >= B[i]){
            return false;
        }
    }
    return true;
}

void sort_row(int *A, int num_cols){
    // Bubblesort
    int n = num_cols;
    while(n >= 0){
        int newn = n==0?-1:0;
        for(int i=1; i < n; i++){
            if(A[i-1] < A[i]){
                int aux = A[i];
                A[i] = A[i-1];
                A[i-1] = aux;
                newn = i;
            }
        }
        n = newn;
    }
}

void new_edge(Graph& graph, int node_from, int node_to){
    graph[node_from][node_to] = 1;
}
void print_graph(Graph& graph, int num_rows){
    int num_cols = num_rows;
    for(int i=0; i < num_rows; i++){
        for(int j=0;j<num_cols-1;j++){
            std::cout<<graph[i][j]<<" ";
        }
        std::cout<<graph[i][num_cols-1]<<std::endl;
    }
}


bool calculate_max_path(Graph& graph, std::vector<int>& vmax, std::vector<int>& vprev, int num_rows){
    bool all_same = true;
    // std::cout<<"---"<<std::endl;
    for(int i=0; i < num_rows; i++){
        for(int j=0; j < num_rows; j++){
            if(graph[j][i] == 1){
                // If vmax[i] is better, we keep, otherwise we update
                // std::cout<<"Check "<<i<<" "<<j<<" - ";
                if(vmax[j] + 1 > vmax[i]) {
                    // std::cout << "We update: " << j << " before "<< i
                    //     << " (" << vmax[i] << " -> " << vmax[j] + 1 << ")" << std::endl;
                    vmax[i] = vmax[j] +1;
                    vprev[i] = j;
                    all_same = false;
                }

            }

        }
    }
    return all_same;
}


void print_reversed_path(int max_path, int last_v, std::vector<int>& vprev){
    if(max_path){
        print_reversed_path(max_path - 1, vprev[last_v], vprev);
        std::cout<<last_v + 1<<" ";
    }
}
void print_result(std::vector<int>& vmax, std::vector<int>& vprev){
    int max_path = 0;
    int last_v = 0;
    for(int i=0; i < vmax.size(); i++){
        if(vmax[i] > max_path){
            max_path = vmax[i];
            last_v = i;
        }
    }
    max_path += 1;
    // std::cout << "RESULT = = = = = = == == = = " << std::endl;
    std::cout << max_path << std::endl;
    print_reversed_path(max_path, last_v, vprev);
    std::cout<<std::endl;
}

void stack_boxes(int** A, int num_rows, int num_cols){
    // Generate a matrix num_rows x num_cols
    Graph graph(num_rows, std::vector<int>(num_rows));
    for(int i=0; i < num_rows; i++){
        sort_row(A[i], num_cols);
    }

    /*
    for(int i=0; i < num_rows; i++){
        std::cout<<i<<":  ";
        for(int j=0; j < num_cols - 1; j++){
            std::cout<<A[i][j]<<" > ";
        }
        std::cout<<A[i][num_cols - 1]<<std::endl;
    }*/
    for(int i=0; i < num_rows; i++){
        for(int j=i + 1; j < num_rows; j++){
            if(fits(A[i], A[j], num_cols)){
                new_edge(graph, i, j);
            }
            if(fits(A[j], A[i], num_cols)){
                new_edge(graph, j, i);
            }
        }
    }
    // print_graph(graph,num_rows);
    bool finished = false;
    std::vector<int> vmax(num_rows);
    std::vector<int> vprev(num_rows);
    for(int i=0; i < num_rows; i++){
        finished = calculate_max_path(graph, vmax, vprev, num_rows);
        if(finished){
            break;
        }
    }
    print_result(vmax, vprev);
}

//Main will read the input and call stack_boxes (who will print result)
int main(){
    int num_rows, num_cols;
    while(std::cin>>num_rows>>num_cols){
        int **A;
        A = new int*[num_rows];
        for(int row=0; row < num_rows; ++row){
            A[row] = new int[num_cols];
            for(int column=0; column < num_cols; ++column){
                int int_read;
                std::cin>>int_read;
                A[row][column] = int_read;
            }
        }
        if(num_rows){
            stack_boxes(A, num_rows, num_cols);
        } else {
            std::cout<<0<<std::endl<<0<<std::endl;
        }
        for (int row= 0; row < num_rows; ++row){
            delete [] A[row];
        }
        delete [] A;
    }
}
