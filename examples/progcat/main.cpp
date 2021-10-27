#include <stdio.h>

int main(int argc, char *const argv[], char *const envp[]) {
    printf("Meow meow! This program was written by a cat!\n");

    printf("Assert 2 + 2 = 5...\n");

    if (2 + 2 == 5) {
        printf("Awesome! Cats are great programmers!\n");
    } else {
        printf("Hmm... Maybe I should stick to scratching the furniture...\n");
        fprintf(stderr, "Assertion Error! Cats are bad programmers.\n");

        return 12;
    }

    return 0;
}
