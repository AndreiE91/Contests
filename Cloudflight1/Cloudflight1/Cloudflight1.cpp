using namespace std;
#include <iostream>
#include <fstream>
#include <string>

int main()
{
    ifstream fin("level1_5.in");
    ofstream fout("output1_5.txt");

    string message = "If you see this in output.txt, reading from file didn't work.";
    int result = 0;
    getline(fin, message);
    int n = stoi(message);
    for (int i = 0; i < n; ++i) {
        string line;
        getline(fin, line);
        for (int j = 0; j < n; ++j) {
            if (line[j] == 'C') {
                ++result;
            }
        }
    }
    fout << result;
}
