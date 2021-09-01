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

namespace avocat {
    enum msg{
        program_start,
        program_end,
        end_msg,
    };

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

            static void redirect_fd(int from, int to, bool curses=false);

            void set_mode(int mode);

            int get_fd() const;

            void replace_fd(int dest);

            Messenger();
            ~Messenger();
    };

    class Container {
        private:
            std::vector <std::string> history[3];
            static void run_cmd(std::string cmd, Messenger in, Messenger out, Messenger err, int& ret, std::atomic<bool>& ready);
        
        public:
            enum s_key{
                in,
                out,
                err
            };

            std::vector <std::string> & get_history(int key) const;

            Container(std::string cmd);
            ~Container();
    };
}