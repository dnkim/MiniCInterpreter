CC = python3
TESTER = LexParTester.py
TEST_OPT = par
TEST_DIR = testfiles

test:
	@for f in $(notdir $(wildcard $(TEST_DIR)/*.txt)); \
	do $(CC) $(TESTER) $(TEST_OPT) $(TEST_DIR)/$$f $(TEST_DIR)/results/$$f; \
	done

clean:
	@rm -f $(TEST_DIR)/results/*.txt
