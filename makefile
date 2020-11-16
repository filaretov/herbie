.PHONY: clear_output to_html
WAV_FILES = $(shell find out/ -type f -name '*.wav')
MP3_FILES = $(patsubst out/%.wav, out/%.mp3, $(WAV_FILES))
IPY_FILES = $(shell find . -not -path "*/.ipynb_checkpoints/*" -name "*.ipynb")

clear_nb_output: $(IPY_FILES)
	jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace  $^

to_html: $(IPY_FILES)
	jupyter nbconvert $^
	mv *.html -t html/

to_mp3: $(MP3_FILES)
	@echo $^

out/%.mp3: out/%.wav
	ffmpeg -y -i $< $@
