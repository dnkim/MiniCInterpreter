CC = python3
TESTER = LexParTester.py
TEST_OPT = par
TEST_DIR = testfiles

test:
	@for f in $(TEST_DIR)/*; do \
		$(CC) $(TESTER) $(TEST_OPT) $$f $$f.result; \
	done

clean:
	@rm -f $(TEST_DIR)/*.result
