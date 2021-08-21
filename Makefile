BIN_DIR := bin

PRJ := avocat avoexe
BIN := $(addprefix $(BIN_DIR)/,$(PRJ))

all: $(BIN) $(PRJ)

$(BIN): $($@:$(BIN_DIR)/%=%)

$(PRJ): $(BIN_DIR)
	cd $@; make

$(BIN_DIR):
	mkdir -p $@

clean:
	@$(RM) -rv $(BIN_DIR)