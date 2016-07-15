.PHONY:clean test load-testing
clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

test:
	./test_danmu.py

load-testing:
	./load_testing.sh
