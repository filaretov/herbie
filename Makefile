.PHONY: clear_output to_html
WAV_FILES = $(shell find out/ -type f -name '*.wav')
MP3_FILES = $(patsubst out/%.wav, out/%.mp3, $(WAV_FILES))

clear_output:
	jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace  **.ipynb

to_html:
	jupyter nbconvert **.ipynb
	mv *.html -t html/

to_mp3: $(MP3_FILES)
	@echo $^

out/%.mp3: out/%.wav
	ffmpeg -y -i $< $@
