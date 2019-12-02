CC = python3
TESTER = LexParTester.py
TEST_OPT = par
TEST_DIR = testfiles

test:
	@test ! -d $(TEST_DIR)/results && mkdir $(TEST_DIR)/results
	@for f in $(notdir $(wildcard $(TEST_DIR)/*.txt)); \
	do $(CC) $(TESTER) $(TEST_OPT) $(TEST_DIR)/$$f $(TEST_DIR)/results/$$f; \
	done

clean:
	@rm -f $(TEST_DIR)/results/*.txt
