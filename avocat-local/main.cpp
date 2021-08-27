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
    int server_fd;
    struct sockaddr_in local_addr;
    char buff[257];
    uint16_t port;

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

    printf("port number %d\n", ntohs(local_addr.sin_port));

    /* Create description file for daemon */

    /* Closing time */
    if (close(server_fd)) {
        fprintf(stderr, "did not close!\n");
        perror("");
    }

    // int r = daemon(0, 0);
    return 0;
}