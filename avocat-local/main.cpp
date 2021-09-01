/*
 *  avocat-local
 *
 *  This is a daemon which mediates and sometimes interjects between
 *  user-level avocat inquiries and a server.
 * 
 *  Author: Gregory Croisdale
 *  University of Tennessee, Knoxville
 * 
 */

// DEFINITE CHANGE OF HEART
// this probably doesn't need to exist

#include <iostream>
#include <string>

#include <unistd.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>

#include "avocat.hpp"

int main(int argc, char** argv) {
    /* Create server and bind to port */
    int server_fd, port;
    struct sockaddr_in local_addr;
    char buff[BUFF_SIZE];

    bzero(&local_addr, sizeof(local_addr));

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("Socket creation error");
        exit(EXIT_FAILURE);
    }

    local_addr.sin_family = AF_INET;
    local_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    local_addr.sin_port = htons(INADDR_ANY);

    if (bind(server_fd, (struct sockaddr*) &local_addr, sizeof(local_addr))) {
        fprintf(stderr, "Failed to bind port %d: ", (int) local_addr.sin_port);
        perror("");
        exit(EXIT_FAILURE);
    }

    socklen_t len = sizeof(local_addr);
    if (getsockname(server_fd, (struct sockaddr *)&local_addr, &len)) {
        perror("getsockname");
    }

    port = ntohs(local_addr.sin_port);

    printf("Predaemon running on port number %d\n", port);

    /* Create description file for daemon */
    FILE* daemon_desc = nullptr;
    std::string config_loc = std::string(getenv("HOME")) + "/" + CONFIG_LOC;
    if ((daemon_desc = fopen(config_loc.c_str(), "w")) == nullptr) {
        perror("Could not open config file");
        return 1;
    }
    if (fwrite(&port, sizeof(port), 1, daemon_desc) != 1) {
        perror("Could not write to config file");
        return 1;
    }

    /* Closing time */
    if (close(server_fd)) {
        perror("Error closing socket");
    }

    if (1 || daemon(0, 0) != 0) {
        perror("Failed to spawn daemon");
    }
    return 0;
}