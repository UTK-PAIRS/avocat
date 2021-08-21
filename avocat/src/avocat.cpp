#include <iostream>
#include <string>
#include <sstream>
#include <thread>

#include <unistd.h>
#include <signal.h>
#include <ncurses.h>

#include "avocat.hpp"

#define DEBUG if (1)
#define CWD "/mnt/c/Users/Gregory/linhome/Projects/avocat/bin"

#define BUFF_SIZE 512

int p_monitor_cb(char** in, int len);

namespace avocat {
    const std::string cwd(CWD);
    bool add_prefix = true;
    bool msg_in_p = false;

    const std::vector <std::string> & Container::get_history(int key) {
        return history[key];
    }

    Container::Container(std::string shell) {
        // create messengers for in / out / err
        Messenger in;
        Messenger out;
        //Messenger err;

        // Set ncurses settings
        initscr();
        noecho();
        cbreak();
        keypad(stdscr, TRUE);
        nodelay(stdscr, FALSE);

        // child acts as shell, parent monitors child
        if ((child_pid = fork()) != 0) {
            // parent

            // configure messengers
            in.set_mode(Messenger::mode_f::mode_write);
            out.set_mode(Messenger::mode_f::mode_read);
            //err.set_mode(Messenger::mode_f::read);

            // test that in and out fds are correctly configured
            if (fdopen(in.get_fd(), "w") == nullptr) perror("parent fdopen in");;
            if (fdopen(out.get_fd(), "r") == nullptr) perror("parent fdopen out");;

            // redirect messengers
            std::thread redir_stdin(Messenger::redirect_fd, STDIN_FILENO, in.get_fd(), true, nullptr);
            std::thread redir_stdout(Messenger::redirect_fd, out.get_fd(), STDOUT_FILENO, false, nullptr);

            // wait for redirection to finish
            redir_stdin.join();
            redir_stdout.join();
        } else {
            // child

            // configure messengers
            in.set_mode(Messenger::mode_f::mode_read);
            out.set_mode(Messenger::mode_f::mode_write);

            // MAYBE USE TTY SYSCALLS?

            // set "in" messenger to stdin 
            in.replace_fd(STDIN_FILENO);
            stdin = fdopen(in.get_fd(), "r");

            // set "out" messenger to stdout
            out.replace_fd(STDOUT_FILENO);
            stdout = fdopen(out.get_fd(), "w");

            // run shell program
            fprintf(stderr, "%s ended with code %d\n", shell.c_str(), system(shell.c_str()));
        }
    }

    Container::~Container() {
        // upon destructor, kill shell emulator and close ncurses session
        if (child_pid != 0) (void) kill(child_pid, 15);
        endwin();
    }

    void Messenger::redirect_fd(int from, int to, bool curses, int (*callback)(char**, int)) {
        #define ECHOIFCHAR(x) if (x < (((1 << (sizeof(char) * 8)) / 2) - 1)) echochar((char) x)

        // line buffer
        std::string l;
        
        // if in curses mode, use echochar and capture special input
        if (curses) {
            int i;
            while ((i = getch()) && i != '\0') {
                /*if (write(to, &i, sizeof(i)) != sizeof(i)) {
                    fprintf(stderr, "failed to write to fd %d!\n", to);
                    perror("");
                } else {*/
                switch (i) {
                    case KEY_BACKSPACE: {
                        // remove char in terminal
                        echochar('\b');
                        echochar(' ');
                        echochar('\b');

                        // remove character from line buffer if exists
                        if (l.length()) (void) l.pop_back();

                        break;
                    }

                    case '\n': {
                        // create newline and flush line buffer
                        echochar('\n');
                        l.push_back('\n');
                        if (add_prefix) l = "" + l;
                        if (write(to, l.c_str(), l.length()) != l.length()) {
                            fprintf(stderr, "failed to write to fd %d!\n", to);
                            perror("");
                        }
                        l.clear();
                        break;
                    }

                    default: {
                        // by default, add char version of input to buffer
                        // and print to screen if within char range
                        l.push_back((char) i);
                        ECHOIFCHAR(i);
                        break;
                    }
                }
                    //DEBUG {fprintf(stderr, "WRITTEN: %d (%c)\n", i, (char) i);}
            }
        }
        else if (callback != nullptr) {
            char buff[BUFF_SIZE];
            int len;
            while ((len = read(from, buff, BUFF_SIZE - 1)) && buff[0] != '\0') {
                if (callback((char**) &buff, len)) {
                    if (write(to, buff, len) != len) {
                        fprintf(stderr, "failed to write to fd %d!\n", to);
                        perror("");
                    }
                }
            }
        } else {
            char buff[BUFF_SIZE];
            int len;
            while ((len = read(from, buff, BUFF_SIZE - 1)) && buff[0] != '\0') {
                if (write(to, buff, len) != len) {
                    fprintf(stderr, "failed to write to fd %d!\n", to);
                    perror("");
                }
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

    int Messenger::get_fd() {   
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

int p_monitor_cb(char** in, int len) {
    std::string sin = *in;
    int pos;
    if (pos = sin.find(avocat::dlm)) {

    }
}