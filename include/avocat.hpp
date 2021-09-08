/*
 *  avocat.hpp
 *
 *  This is a daemon which mediates and sometimes interjects between
 *  user-level avocat inquiries and 
 * 
 *  Author: Gregory Croisdale
 *  University of Tennessee, Knoxville
 */

#include <vector>
#include <string>
#include <atomic>

#include <stdint.h>

#define BUFF_SIZE 512
#define CONFIG_LOC ".avocat/config"

#define PORT 8123

namespace avocat {
    class Messenger {
        private:
            int in;
            int out;
            int mode;

        public:
            enum mode_f{
                mode_read,
                mode_write
            };

            static void redirect_fd(int from, int to, std::string& history);

            void set_mode(int mode);

            int get_fd() const;

            void replace_fd(int dest);

            Messenger();
            ~Messenger();
    };

    int execute_command(int argc, char *const argv[], char *const envp[], std::string history[2]);

    struct ErrorDesc {
        std::vector<std::string> argv;
        std::string out;
        std::string err;

        int ret;
    };
}