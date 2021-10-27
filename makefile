
TEST_SH        := $(wildcard test/*.sh)

TEST_STDOUT    := $(subst .sh,.stdout,$(TEST_SH))


.PHONY: all FORCE

all: $(TEST_STDOUT)

test/%.stdout: test/%.sh FORCE
	-sh $< >$@ 2>$(subst .stdout,.stderr,$@)




