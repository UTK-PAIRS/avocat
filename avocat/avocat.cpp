#include <iostream>
#include <string>
#include <thread>
#include <vector>
#include <atomic>

#include <unistd.h>
#include <signal.h>
#include <sys/wait.h> 

#include "avocat.hpp"

#define DEBUG if (0)

namespace avocat {
    // This is a local instance of avocat
    void Messenger::redirect_fd(int from, int to, std::string& history) {
        char buff[BUFF_SIZE];
        int len;
        while ((len = read(from, buff, BUFF_SIZE - 1)) && buff[0] != '\0') {
            if (len < 0) {
                fprintf(stderr, "failed to write from fd %d!\n", from);
                perror("");
            }
            if (write(to, buff, len) != len) {
                fprintf(stderr, "failed to write to fd %d!\n", to);
                perror("");
            }
            history += buff;
        }
    }

    Messenger::Messenger() {
        // create and populate pipes
        int fd[2];
        if (pipe(fd)) {
            fprintf(stderr, "Error opening pipe!\n");
            perror("messenger constructor pipe");
        }

        in = fd[1];
        out = fd[0];

        DEBUG {printf("Messenger created with fds %d and %d\n", in, out);}

        // set mode to -1 to start
        mode = -1;
    }

    Messenger::~Messenger() {
        // close appropriate file descriptors according to mode
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
        // sets mode and allows messenger to be used
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

    int Messenger::get_fd() const {   
        // fd that is in use     
        if (mode == mode_f::mode_read) {
            return out;
        } else if (mode == mode_f::mode_write) {
            return in;
        } else {
            return -1;
        }
    }

    void Messenger::replace_fd(int fd) {
        // replace input fd with messenger's (ex., set messenger to stdin) 
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

    int execute_command(int argc, char *const argv[], char *const envp[], std::string history[2]) {
        Messenger out;
        Messenger err;

        int childpid;

        if (childpid = fork()) {
            // parent
            int status = 0;

            out.set_mode(Messenger::mode_f::mode_read);
            err.set_mode(Messenger::mode_f::mode_read);

            std::thread redir_out(Messenger::redirect_fd, out.get_fd(), STDOUT_FILENO, std::ref(history[0])); 
            std::thread redir_err(Messenger::redirect_fd, err.get_fd(), STDERR_FILENO, std::ref(history[1])); 

            while (wait(&status) > 0);

            redir_out.join();
            redir_err.join();

            return WEXITSTATUS(status);
        } else {
            // child
            int status = 0;

            out.set_mode(Messenger::mode_f::mode_write);
            err.set_mode(Messenger::mode_f::mode_write);

            out.replace_fd(STDOUT_FILENO);
            err.replace_fd(STDERR_FILENO);

            if (execvpe(argv[1], argv + 1, envp)) {
                while (wait(&status) > 0);
                fprintf(stderr, "STAT: %d\n", status);
                return WEXITSTATUS(status);
            }

            return 69;
        }
    }
}