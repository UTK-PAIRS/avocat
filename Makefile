BIN_DIR := bin
CONFIG_DIR := ~/.avocat

PRJ := avocat avocat-local avocat-db
BIN := $(addprefix $(BIN_DIR)/,$(PRJ))

all: $(BIN) $(PRJ)

$(BIN): $($@:$(BIN_DIR)/%=%)

$(PRJ): $(BIN_DIR) $(CONFIG_DIR)
	cd $@; echo $@; make

$(BIN_DIR) $(CONFIG_DIR):
	mkdir -p $@

clean:
	@$(RM) -rv $(BIN_DIR)