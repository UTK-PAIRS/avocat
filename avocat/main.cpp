/*
    Avocat instances.
        Called by user in the command line to use the
        program.
*/

#include <iostream>
#include <string>

#include "avocat.hpp"

using namespace std;


//  Placeholder //
int main(int argc, char *argv[])
{
    /*
    string combinedArgs;

    //  Check argc  //
    if(argc <= 1)
    {
    cerr << "Not enough arguments.\n";
    return 1;
    }

    //  Assigns first string    //
    combinedArgs = argv[1];

    //  Loop through string //
    for(int i = 1; i < argc; i++)
    {
    combinedArgs += ' ';
    combinedArgs +=  argv[i];
    }    

    system(combinedArgs.c_str());
    */

    avocat::Container("echo this is a test");

    return 0;
}
