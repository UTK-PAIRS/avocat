#include <iostream>
#include <thread>
#include <string>

#include <unistd.h>
#include <string.h>

#include "avocat.hpp"

using namespace std;

int main(int argc, char** argv) {
    // if nothing was passed, immediately return
    if (argc < 2) return 1;

    // prevent avoexe recursion by removing arguments identical to argv[0]
    int i;
    for (i = 1; i < argc; i++) {
        if (strcmp(argv[0], argv[i])) break;
    }
    if (i >= argc) return 2;

    // create combined string for system call
    string combined(argv[i]);
    for (i++; i < argc; i++) combined += string(" ") + argv[i];

    //cout << "EXECUTING THE FOLLOWING: " << combined << '\n';

    // send secret messages to avocat
    printf("%s %d %d", avocat::dlm, avocat::msg::program_start, avocat::msg::end_msg);
    fflush(stdout);

    // execute desired command
    int status = system(combined.c_str());

    // send even more secret messages to avocat
    printf("%s %d %d %d", avocat::dlm, avocat::msg::program_end, status, avocat::msg::end_msg);
    fflush(stdout);

    return status;
}