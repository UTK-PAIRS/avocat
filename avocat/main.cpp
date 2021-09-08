/*
    Avocat instances.
        Called by user in the command line to use the
        program.
*/

#include <iostream>
#include <string>
#include <curl/curl.h>

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
        printf("\n=== AVOCAT ===\n");
        // return value was nonzero!
        printf("%.20s finished with error code %d!\n", argv[1], ret);

        // now we need to connect to the daemon
        printf("Diagnosing...\n");
    } else {
        printf("\n=== AVOCAT ===\n");
            printf("%.20s finished execution successfully! (ret: %d)\n", argv[1], ret);
    }
    
    return 0;
}
