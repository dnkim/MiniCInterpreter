CC = python3
TESTER = src/MiniCInterpreter.py
TEST_OPT = test
TEST_DIR = testfiles

test:
	@mkdir -p $(TEST_DIR)/results
	@for f in $(notdir $(wildcard $(TEST_DIR)/*.txt)); do \
		$(CC) $(TESTER) $(TEST_DIR)/$$f $(TEST_OPT) > $(TEST_DIR)/results/$$f; \
	done

clean:
	@rm -rf $(TEST_DIR)/results
	@rm -rf src/__pycache__
