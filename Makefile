CC = python3
TESTER = Interpreter.py
TEST_DIR = testfiles

test:
	@mkdir -p $(TEST_DIR)/results
	@for f in $(notdir $(wildcard $(TEST_DIR)/*.txt)); do \
		$(CC) $(TESTER) $(TEST_DIR)/$$f > $(TEST_DIR)/results/$$f; \
	done

clean:
	@rm -rf $(TEST_DIR)/results
