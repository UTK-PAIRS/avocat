#include <vector>
#include <string>

namespace avocat {
    const char dlm[] = "!?!AVOCAT_DEL!?!";

    enum msg{
        program_start,
        program_end,
        end_msg,
    };

    class Container {
        private:
            std::vector <std::string> history[3];

            int child_pid;
        public:
            enum s_key{
                in,
                out,
                err
            };

            const std::vector <std::string> & get_history(int key);

            Container(std::string);
            ~Container();
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

            static void redirect_fd(int from, int to, bool curses=false, int (*callback)(char**, int) = nullptr);

            void set_mode(int mode);

            int get_fd();

            void replace_fd(int dest);

            Messenger();
            ~Messenger();
    };
}