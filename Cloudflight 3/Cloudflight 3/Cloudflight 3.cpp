using namespace std;
#include <iostream>
#include <fstream>
#include <string>

int main()
{
    ifstream fin("level3_1.in");
    ofstream fout("output3_1.txt");

    string message = "If you see this in output.txt, reading from file didn't work.";
    int result = 0;
    bool died = false;
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

    --pRow; --pCol;
    string movement, nrGhs;
    getline(fin, movement);

    getline(fin, nrGhs);
    int nrGhosts = stoi(nrGhs);

    string* ghostMovements = new string[nrGhosts];
    int* ghostMovementLengths = new int[nrGhosts];
    int* ghostRows = new int[nrGhosts];
    int* ghostCols = new int[nrGhosts];


    for (int i = 0; i < nrGhosts; ++i) {

        int tRow, tCol;
        string temp, tnum;
        getline(fin, temp);
        int k = 0;

        while (temp[k] != ' ') {
            tnum += temp[k];
            ++k;
        }
        tRow = stoi(tnum);
        tnum = "";
        ++k;
        while (k < temp.length()) {
            tnum += temp[k];
            ++k;
        }
        tCol = stoi(tnum);

        getline(fin, temp);
        int tseqLen = stoi(temp);

        --tRow; --tCol;
        ghostMovementLengths[i] = tseqLen;
        ghostRows[i] = tRow;
        ghostCols[i] = tCol;
        string tmovement;
        getline(fin, tmovement);
        ghostMovements[i] = tmovement;
    }

    for (int i = 0; i < seqLen && !died; ++i) {
        for (int j = 0; j < nrGhosts && !died; ++j) {
            switch (ghostMovements[j][i]) {
            case 'L': {
                if ((board[ghostRows[j]])[ghostCols[j] - 1] != 'W' && (board[ghostRows[j]])[ghostCols[j] - 1] != 'G') {
                    board[ghostRows[j]][ghostCols[j]] = board[ghostRows[j]][ghostCols[j] - 1];
                    board[ghostRows[j]][ghostRows[j] - 1] = 'G';
                    if ((board[ghostRows[j]])[ghostCols[j] - 1] == 'P') {
                        died = true;
                    }
                    --ghostCols[j];
                }
                break;
            }
            case 'R': {
                if ((board[ghostRows[j]])[ghostCols[j] + 1] != 'W' && (board[ghostRows[j]])[ghostCols[j] + 1] != 'G') {
                    board[ghostRows[j]][ghostCols[j]] = board[ghostRows[j]][ghostCols[j] + 1];
                    board[ghostRows[j]][ghostCols[j] + 1] = 'G';
                    if ((board[ghostRows[j]])[ghostCols[j] + 1] == 'P') {
                        died = true;
                    }
                    ++ghostCols[j];
                }
                break;
            }
            case 'U': {
                if ((board[ghostRows[j] - 1])[ghostCols[j]] != 'W' && (board[ghostRows[j] - 1])[ghostCols[j]] != 'G') {
                    board[ghostRows[j]][ghostCols[j]] = board[ghostRows[j] - 1][ghostCols[j]];
                    board[ghostRows[j] - 1][ghostCols[j]] = 'G';
                    if ((board[ghostRows[j] - 1])[ghostCols[j]] == 'P') {
                        died = true;
                    }
                    --ghostRows[j];
                }
                break;
            }
            case 'D': {
                if ((board[ghostRows[j] + 1])[ghostCols[j]] != 'W' && (board[ghostRows[j] + 1])[ghostCols[j]] != 'G') {
                    board[ghostRows[j]][ghostCols[j]] = board[ghostRows[j] + 1][ghostCols[j]];
                    board[ghostRows[j] + 1][ghostCols[j]] = 'G';
                    if ((board[ghostRows[j] + 1])[ghostCols[j]] == 'P') {
                        died = true;
                    }
                    + ghostRows[j];
                }
                break;
            }
            default: {
                cout << "Nu ii ok \n";
                break;
            }
            }
        }
        switch (movement[i]) {
        case 'L': {
            if ((board[pRow])[pCol - 1] != 'W') {
                board[pRow][pCol] = (board[pRow])[pCol - 1];
                board[pRow][pCol - 1] = 'P';
                --pCol;
            }
            if ((board[pRow])[pCol] == 'G') {
                died = true;
            }
            if ((board[pRow])[pCol] == 'C') {
                (board[pRow])[pCol] = ' ';
            }
            break;
        }
        case 'R': {
            if ((board[pRow])[pCol + 1] != 'W') {
                board[pRow][pCol] = (board[pRow])[pCol - 1];
                board[pRow][pCol + 1] = 'P';
                ++pCol;
            }
            if ((board[pRow])[pCol] == 'G') {
                died = true;
            }
            if ((board[pRow])[pCol] == 'C') {
                (board[pRow])[pCol] = ' ';
            }
            break;
        }
        case 'U': {
            if ((board[pRow - 1])[pCol] != 'W') {
                board[pRow][pCol] = (board[pRow - 1])[pCol];
                board[pRow - 1][pCol] = 'P';
                --pRow;
            }
            if ((board[pRow])[pCol] == 'G') {
                died = true;
            }
            if ((board[pRow])[pCol] == 'C') {
                (board[pRow])[pCol] = ' ';
            }
            break;
        }
        case 'D': {
            if ((board[pRow + 1])[pCol] != 'W') {
                board[pRow][pCol] = (board[pRow + 1])[pCol];
                board[pRow + 1][pCol] = 'P';
                --pRow;
            }
            if ((board[pRow])[pCol] == 'G') {
                died = true;
            }
            if ((board[pRow])[pCol] == 'C') {
                (board[pRow])[pCol] = ' ';
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
            if ((board[i])[j] == ' ') {
                ++result;
            }
        }

    }
    if (died) {
        fout << result << " YES";
    }
    else {
        fout << result << " NO";

    }
    

}
