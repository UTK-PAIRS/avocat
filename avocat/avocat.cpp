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
        char buff[BUFF_SIZE]; // buffer taken from input fd
        int len;              // length of message from input fd

        // keep reading all of the possible messages
        while ((len = read(from, buff, BUFF_SIZE - 1)) && buff[0] != '\0') {
            // error check i/o
            if (len < 0) {
                fprintf(stderr, "failed to write from fd %d!\n", from);
                perror("");
            }
            if (write(to, buff, len) != len) {
                fprintf(stderr, "failed to write to fd %d!\n", to);
                perror("");
            }

            // add string to history
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

        // set mode to -1 to start -- invalid in all applications
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
        // set mode, allowing pipe to be used 
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
        // return fd used by mode    
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
        if (mode == mode_f::mode_read) {
            in = fd;
        } else if (mode == mode_f::mode_write) {
            out = fd;
        } else {
            return;
        }

        // use dup2 to replace designated fd
        if (dup2(get_fd(), fd) == -1) {
            fprintf(stderr, "dupe machine broke!\n");
            perror("");
            return;
        }
    }

    int execute_command(int argc, char *const argv[], char *const envp[], std::string history[2]) {
        /* 
         * Function: avocat::execute_command
         * =================================
         * Runs a command
         */
        Messenger out;
        Messenger err;

        int childpid;

        // create fork, parent monitors, child runs program
        if (childpid = fork()) {
            // parent
            int status = 0;

            // use messengers to redirect child streams to parent streams with saved history
            out.set_mode(Messenger::mode_f::mode_read);
            err.set_mode(Messenger::mode_f::mode_read);
            std::thread redir_out(Messenger::redirect_fd, out.get_fd(), STDOUT_FILENO, std::ref(history[0])); 
            std::thread redir_err(Messenger::redirect_fd, err.get_fd(), STDERR_FILENO, std::ref(history[1])); 

            // wait for child to finish and then end redirection threads
            while (wait(&status) > 0);
            redir_out.join();
            redir_err.join();

            // return using the error status of child
            return WEXITSTATUS(status);
        } else {
            // child
            int status = 0;
            
            // use messengers and replace stderr/out
            out.set_mode(Messenger::mode_f::mode_write);
            err.set_mode(Messenger::mode_f::mode_write);
            out.replace_fd(STDOUT_FILENO);
            err.replace_fd(STDERR_FILENO);

            // run program with args and envp
            execvpe(argv[0], argv + 0, envp);
            // execution after this point means exevpe failed
            fprintf(stderr, "Could not execute %.20s!\n", argv[1]);
            perror("");

            return -1;
        }
    }
}