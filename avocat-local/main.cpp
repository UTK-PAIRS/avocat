#include <iostream>
#include <string>

#include <unistd.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>

int main(int argc, char** argv) {
    int server_fd;
    struct sockaddr local_addr;
    char buffer[256];

    if (!(server_fd = socket(AF_INET, SOCK_STREAM, 0))) {
        perror("Socket creation error");
        exit(EXIT_FAILURE);
    }

    if (bind(server_fd, &local_addr, INADDR_ANY)) {
        fprintf(stderr, "Failed to bind port %d: ", *((unsigned short*) (((char*) &local_addr) + sizeof(short))));
        perror("");
        exit(EXIT_FAILURE);
    }

    // int r = daemon(0, 0);
    return 0;
}