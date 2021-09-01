#include <iostream>
#include <string>
#include <thread>
#include <vector>
#include <atomic>

#include <unistd.h>
#include <signal.h>

#include "avocat.hpp"

#define DEBUG if (1)
#define BUFF_SIZE 512

namespace avocat {

    std::vector <std::string>& Container::get_history(int key) const {
        return ((std::vector <std::string>* const) history)[key];
    }

    Container::Container(std::string cmd) {
        // create messengers for in / out / err
        Messenger in;
        Messenger out;
        Messenger err;

        int ret = -1;                     // return value of thread
        std::atomic <bool> ready(false);  // parent is ready for cmd execution

        // create execution thread
        std::thread runner(Container::run_cmd, cmd, in, out, err, std::ref(ret), std::ref(ready));

        // redirect
        std::thread redir_stdin(Messenger::redirect_fd, STDIN_FILENO, in.get_fd(), true);
        std::thread redir_stdout(Messenger::redirect_fd, out.get_fd(), STDOUT_FILENO, false);

        in.set_mode(Messenger::mode_f::mode_write);
        out.set_mode(Messenger::mode_f::mode_read);

        // indicate readiness to thread
        ready = true;

        /*
        if ((child_pid = fork()) != 0) {
            // parent

            // configure messengers
            in.set_mode(Messenger::mode_f::mode_write);
            out.set_mode(Messenger::mode_f::mode_read);
            //err.set_mode(Messenger::mode_f::read);

            // test that in and out fds are correctly configured
            if (fdopen(in.get_fd(), "w") == nullptr) perror("parent fdopen in");
            if (fdopen(out.get_fd(), "r") == nullptr) perror("parent fdopen out");

            // redirect messengers
            std::thread redir_stdin(Messenger::redirect_fd, STDIN_FILENO, in.get_fd(), true, nullptr);
            std::thread redir_stdout(Messenger::redirect_fd, out.get_fd(), STDOUT_FILENO, false, nullptr);

            // wait for redirection to finish
            redir_stdin.join();
            redir_stdout.join();

            int status;
     
            waitpid(pid, &status, 0);
        } else {
            // child

            // configure messengers
            in.set_mode(Messenger::mode_f::mode_read);
            out.set_mode(Messenger::mode_f::mode_write);

            exit(system(cmd));
        }
        */
       runner.join();
       redir_stdin.join();
       redir_stdout.join();
    }

    Container::~Container() {
    }

    void Container::run_cmd(std::string cmd, Messenger in, Messenger out, Messenger err, int& ret, std::atomic<bool>& ready) {
        in.set_mode(Messenger::mode_f::mode_read);
        out.set_mode(Messenger::mode_f::mode_write);

        while (!ready.load());

        // set "in" messenger to stdin 
        in.replace_fd(STDIN_FILENO);
        stdin = fdopen(in.get_fd(), "r");

        // set "out" messenger to stdout
        out.replace_fd(STDOUT_FILENO);
        stdout = fdopen(out.get_fd(), "w");

        std::cout << "yooo we gucci gang\n";
    }

    void Messenger::redirect_fd(int from, int to, bool curses) {
        // line buffer
        std::string l;
        
        char buff[BUFF_SIZE];
        int len;
        while ((len = read(from, buff, BUFF_SIZE - 1)) && buff[0] != '\0') {
            if (write(to, buff, len) != len) {
                fprintf(stderr, "failed to write to fd %d!\n", to);
                perror("");
            }
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
}