SUBDIRS = vk

all:
	for dir in $(SUBDIRS); do \
		make -C $$dir; \
	done

clean:
	for dir in $(SUBDIRS); do \
		make -C $$dir clean; \
	done

info:
	python vkInfo.py

test: ../shader/echo.spv
	python vkComputeSample.py

