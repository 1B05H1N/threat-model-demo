PY       ?= python
MODEL    = threatmodel/model.py

.PHONY: run model clean test setup diagrams

run:
	$(PY) src/app.py

model:
	$(PY) $(MODEL) --dfd --seq --report threats.md > model_output.txt

# Extract PlantUML and Graphviz code and generate diagrams
diagrams: model
	awk '/@startuml/,/@enduml/' model_output.txt > sequence.puml
	awk '/digraph tm {/,/}/' model_output.txt > dfd.dot
	plantuml sequence.puml
	dot -Tpng dfd.dot -o dfd.png

clean:
	rm -f *.png threats.md

test:
	$(PY) -m pytest tests/

setup:
	$(PY) -m venv venv
	. venv/bin/activate && pip install -r requirements.txt 