#include <iostream>

#include "avocat.hpp"

using namespace std;

int main() {
    string shell;

    do {
        if (cin.eof()) break;
        cout << "Enter desired shell command (for example, bash -i): ";
    } while (getline(cin, shell) && (shell.length() == 0));

    avocat::Container c(shell);
    
    return 0;
}