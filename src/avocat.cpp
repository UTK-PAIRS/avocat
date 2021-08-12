#include <iostream>
#include <thread>

#include <unistd.h>
#include <signal.h>

#include "avocat.hpp"

#define DEBUG if (1)

#define BUFF_SIZE 512

namespace avocat {
    const std::vector <std::string> & Container::get_history(int key) {
        return history[key];
    }

    Container::Container(std::string shell) {
        Messenger in;
        Messenger out;
        //Messenger err;

        if ((child_pid = fork()) != 0) {
            // parent
            in.set_mode(Messenger::mode_f::mode_write);
            out.set_mode(Messenger::mode_f::mode_read);
            //err.set_mode(Messenger::mode_f::read);

            // test that in and out fds are correctly configured
            if (fdopen(in.get_fd(), "w") == nullptr) perror("parent fdopen in");;
            if (fdopen(out.get_fd(), "r") == nullptr) perror("parent fdopen out");;

            std::thread redir_stdin(Messenger::redirect_fd, STDIN_FILENO, in.get_fd());
            std::thread redir_stdout(Messenger::redirect_fd, out.get_fd(), STDOUT_FILENO);

            redir_stdin.join();
            redir_stdout.join();
        } else {
            // child
            in.set_mode(Messenger::mode_f::mode_read);
            out.set_mode(Messenger::mode_f::mode_write);

            int ttymaster, ttyslave, pid;

            // set "in" messenger to stdin 
            in.replace_fd(STDIN_FILENO);
            stdin = fdopen(in.get_fd(), "r");

            // set "out" messenger to stdout
            out.replace_fd(STDOUT_FILENO);
            stdout = fdopen(out.get_fd(), "w");

            fprintf(stderr, "%s ended with code %d\n", shell.c_str(), system(shell.c_str()));
        }
    }

    Container::~Container() {
        if (child_pid != 0) (void) kill(child_pid, 15);
        return;
    }

    void Messenger::redirect_fd(int from, int to) {
        char buff[BUFF_SIZE];
        int len;

        while ((len = read(from, buff, BUFF_SIZE - 1)) && buff[0] != '\0') {
            if (write(to, buff, len) != len) {
                fprintf(stderr, "failed to write to fd %d!\n", to);
                perror("");
            } else {
                //DEBUG {fprintf(stderr, "WRITTEN: %c\n", c[0]);}
            }
        }
    }

    Messenger::Messenger() {
        int fd[2];
        
        if (pipe(fd)) {
            fprintf(stderr, "Error opening pipe!\n");
            perror("messenger constructor pipe");
        }

        in = fd[1];
        out = fd[0];

        DEBUG {printf("Messenger created with fds %d and %d\n", in, out);}

        mode = -1;
    }

    Messenger::~Messenger() {
        // make sure to close appropriate file descriptors
        if (mode == mode_f::mode_read) {
            close(out);
        } else if (mode == mode_f::mode_write) {
            close(in);
        } else {
            close(out);
            close(in);
        }
    }

    void Messenger::set_mode(int mode) {
        DEBUG {printf("Setting mode to %d\n", mode);}
        
        if (mode == mode_f::mode_read) {
            close(in);
            in = -1;

        } else if (mode == mode_f::mode_write) {
            close(out);
            out = -1;

        } else {
            fprintf(stderr, "invalid mode %d!\n", mode);
            return;
        }

        this->mode = mode;
    }

    int Messenger::get_fd() {        
        if (mode == mode_f::mode_read) {
            return out;
        } else if (mode == mode_f::mode_write) {
            return in;
        } else {
            return -1;
        }
    }

    void Messenger::replace_fd(int fd) {
        DEBUG {printf("Replacing fd %d with %d\n", fd, get_fd());}
        if (mode == mode_f::mode_read) {
            in = fd;
        } else if (mode == mode_f::mode_write) {
            out = fd;
        } else {
            return;
        }

        if (dup2(get_fd(), fd) == -1) {
            fprintf(stderr, "dupe machine broke!\n");
            perror("");
            return;
        }
    }
}