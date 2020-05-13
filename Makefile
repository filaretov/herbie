.PHONY: clear html

clear:
	jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace  **.ipynb

html:
	jupyter nbconvert **.ipynb
	mv *.html -t html/
