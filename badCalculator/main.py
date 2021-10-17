"""
    Author: Chase
    Desc: A unit converter made incorrect on purpose so as ot generate errors
"""
import sys


def main():
    l = sys.argv[1:]
    calc = Calculator(l)
    


class Calculator:

    def __init__(self, input: list) -> None:

        self.input = input
        
        if self.input == ["--help"]:
            self.runHelp()
        
        self.run()
        
    def run(self) -> None:

        if len(self.input) != 3:
            exit("ERROR INCORRECT NUM OF ARGS")

        unitOne = float(self.input[2])


        #   Branches    #
        if self.input[0] == "USD":
            if self.input[1] == "YEN":
                tmp = unitOne * 114.38
                print(unitOne, " USD is worth ", tmp, " Yen")

        elif self.input[0] == "YEN":
            if self.input[1] == "USD":
                tmp = unitOne / 114.38
                print(unitOne, " Yen is worth ", tmp, " USD")
        
        elif self.input[0] == "METERS":
            if self.input[1] == "FEET":
                tmp = unitOne / 3.28084
                print(unitOne, " Meters is ", tmp, " feet")

        elif self.input[0] == "FEET":
            if self.input[1] == "METERS":
                tmp = unitOne * 3.28084
                print(unitOne, " Feet is ", tmp, " meters")

        else:
            print("Incorrect units") 
            exit()       


    def runHelp(self) -> None:
        print("FORMAT:")
        print("[FIRST TYPE] [SECOND TYPE] [AMOUNT]\n")
        print("CONVERSATIONS AVAIABLE:")
        print("MONEY:")
        print("   USD\n   YEN\n")
        print("MEASUREMENT:")
        print("   FEET\n   METERS")
        exit()

    



if __name__ == "__main__":
    main()