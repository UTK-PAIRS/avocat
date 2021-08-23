BIN_DIR := bin

PRJ := avocat avocat-local avocat-db
BIN := $(addprefix $(BIN_DIR)/,$(PRJ))

all: $(BIN) $(PRJ)

$(BIN): $($@:$(BIN_DIR)/%=%)

$(PRJ): $(BIN_DIR)
	cd $@; echo $@; make

$(BIN_DIR):
	mkdir -p $@

clean:
	@$(RM) -rv $(BIN_DIR)