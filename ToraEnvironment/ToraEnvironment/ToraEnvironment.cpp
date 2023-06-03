using namespace std;
#include <iostream>
#include <fstream>
#include <string>

int main()
{
    ifstream fin("Level1_sample");
    ofstream fout("Output1_sample.txt");

    string message = "If you see this in output.txt, reading from file didn't work.";

    getline(fin, message);
    int n = stoi(message);
    for (int i = 0; i < n; ++i) {
        string line;
        getline(fin, line);
        for (int j = 0; j < n; ++j) {
            if (line[j] == 'C') {
            }
        }
    }
}

