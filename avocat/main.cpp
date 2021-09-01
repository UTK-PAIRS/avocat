/*
    Avocat instances.
        Called by user in the command line to use the
        program.
*/

#include <iostream>
#include <string>

#include "avocat.hpp"

using namespace std;


int main(int argc, char *const argv[], char *const envp[])
{
    if (argc < 2) {
        fprintf(stderr, "Usage: %.20s cmd args...\n", argv[0]);
        return 0;
    }

    string history[2] = {"", ""};
    int ret;

    if ((ret = avocat::execute_command(argc, argv, envp, history)) != 0) {
        // return value was nonzero!
        printf("%.20s finished with error code %d!\n", argv[1], ret);

        // now we need to connect to the daemon
        printf("Diagnosing...\n");
    }

    cout << "from stdout: " << history[0];
    cout << "from stderr: " << history[1];

    return 0;
}
