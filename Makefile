PY=python
SCRIPTPATH=scripts/

build: clean check qms

qms: $(SCRIPTPATH)quick_map_server.py
	$(PY) $(SCRIPTPATH)quick_map_server.py -i icons/ -d datasource/ -b build/

check: $(SCRIPTPATH)datasource_validate.py
	$(PY) $(SCRIPTPATH)datasource_validate.py -s schema.json -d datasource/

clean:
	rm -rf build/*
  