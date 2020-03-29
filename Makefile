
NAME = debian_watcher

bootstrap:
	python3 -m venv venv
	./venv/bin/pip3 install -r requirements.txt
	./venv/bin/pip3 install pytest
	mkdir storage

docker-build:
	docker build --tag $(NAME) .

docker-run:
	docker run --rm $(NAME)

debug-docker-run:
	docker run -it --rm -v $(PWD)/test.py:/main.py -v $(PWD)/$(NAME)/:/$(NAME)/ -v $(PWD)/storage/:/storage/ $(NAME)

run:
	./venv/bin/python3 main.py


tests:
	./venv/bin/pytest

.PHONY: tests
