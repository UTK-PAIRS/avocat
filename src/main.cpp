#include <iostream>

#include "avocat.hpp"

using namespace std;

int main(int argc, char** argv) {
    string shell;

    if (argc < 2 || string(argv[1]) != "-d") {
        do {
            cout << "Enter desired shell command (for example, bash -i): ";
        } while (getline(cin, shell) && (shell.length() == 0));  
    } else shell = "bash";

    if (cin.eof()) return 0;

    avocat::Container c(shell);
    
    return 0;
}