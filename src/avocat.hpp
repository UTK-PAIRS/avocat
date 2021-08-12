#include <vector>
#include <string>

namespace avocat {
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

            static void redirect_fd(int from, int to);

            void set_mode(int mode);

            int get_fd();

            void replace_fd(int dest);

            Messenger();
            ~Messenger();
    };
}