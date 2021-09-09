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

    if ((ret = avocat::execute_command(argc - 1, argv + 1, envp, history)) != 0) {
        printf("\n=== AVOCAT ===\n");
        // return value was nonzero!
        printf("%.20s finished with error code %d!\n", argv[1], ret);

        // now we need to connect to the daemon / db
        printf("Diagnosing... While we wait, here is the source code for example.com!\n");

        // https://curl.se/libcurl/c/simple.html
        CURL *curl;
        CURLcode res;

        curl = curl_easy_init();
        if(curl) {
            curl_easy_setopt(curl, CURLOPT_URL, "https://example.com");
            /* example.com is redirected, so we tell libcurl to follow redirection */
            curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

            /* Perform the request, res will get the return code */
            res = curl_easy_perform(curl);
            /* Check for errors */
            if(res != CURLE_OK)
                fprintf(stderr, "curl_easy_perform() failed: %s\n",
                    curl_easy_strerror(res));

            /* always cleanup */
            curl_easy_cleanup(curl);
        }

    } else {
        printf("\n=== AVOCAT ===\n");
            printf("%.20s finished execution successfully! (ret: %d)\n", argv[1], ret);
    }
    
    return 0;
}