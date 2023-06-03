using namespace std;
#include <iostream>
#include <fstream>
#include <string>

int main()
{
    ifstream fin("level2_5.in");
    ofstream fout("output2_5.txt");

    string message = "If you see this in output.txt, reading from file didn't work.";
    int result = 0;
    getline(fin, message);
    int n = stoi(message);
    string* board = new string[n];
    for (int i = 0; i < n; ++i) {
        string line;
        getline(fin, line);
        board[i] = line;
    }
    string pos, number;
    int pRow, pCol;
    getline(fin, pos);
    int k = 0;
    while (pos[k] != ' ') {
        number += pos[k];
        ++k;
    }
    pRow = stoi(number);
    number = "";
    ++k;
    while (k < pos.length()) {
        number += pos[k];
        ++k;
    }
    pCol = stoi(number);
    
    getline(fin, pos);
    int seqLen = stoi(pos);

    string* visited = new string[n];
    for (int i = 0; i < n; ++i) {
        visited[i] = board[i];
    }

    --pRow; --pCol;
    string movement;
    getline(fin, movement);
    for (int i = 0; i < seqLen; ++i) {
        switch (movement[i]) {
            case 'L': {
                if ((board[pRow])[pCol - 1] != 'W') {
                    --pCol;
                }
                if ((visited[pRow])[pCol] == 'C') {
                    (visited[pRow])[pCol] = ' ';
                }
                break;
            }
            case 'R': {
                if ((board[pRow])[pCol + 1] != 'W') {
                    ++pCol;
                }
                if ((visited[pRow])[pCol] == 'C') {
                    (visited[pRow])[pCol] = ' ';
                }
                break;
            }
            case 'U': {
                if ((board[pRow - 1])[pCol] != 'W') {
                    --pRow;
                }
                if ((visited[pRow])[pCol] == 'C') {
                    (visited[pRow])[pCol] = ' ';
                }
                break;
            }
            case 'D': {
                if ((board[pRow + 1])[pCol] != 'W') {
                    ++pRow;
                }
                if ((visited[pRow])[pCol] == 'C') {
                    (visited[pRow])[pCol] = ' ';
                }
                break;
            }
            default: {
                cout << "Nu ii ok \n";
                break;
            }
        }
    }

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if ((visited[i])[j] == ' ') {
                ++result;
            }
        }
    }
    fout << result;
}
