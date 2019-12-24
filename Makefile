CC = python3
TESTER = src/MiniCInterpreter.py
TEST_OPT = -t
RTEST_OPT = -t -r
TEST_DIR = testfiles

test:
	@mkdir -p $(TEST_DIR)/results
	@for f in $(notdir $(wildcard $(TEST_DIR)/*.txt)); do \
		$(CC) $(TESTER) $(TEST_OPT) $(TEST_DIR)/$$f > $(TEST_DIR)/results/$$f; \
	done

rtest:
	@mkdir -p $(TEST_DIR)/results
	@for f in $(notdir $(wildcard $(TEST_DIR)/*.txt)); do \
		$(CC) $(TESTER) $(RTEST_OPT) $(TEST_DIR)/$$f > $(TEST_DIR)/results/$$f; \
	done

clean:
	@rm -rf $(TEST_DIR)/results
	@rm -rf src/__pycache__
