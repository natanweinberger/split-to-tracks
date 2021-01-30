build:
	docker build -t split-tracks .

dev:
	docker run --rm -it -v $(shell pwd):/var/src -v $(YTMP3_OUTPUT_DIR):/home split-tracks bash