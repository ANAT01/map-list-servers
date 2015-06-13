PY=python
SCRIPTPATH=scripts/
BLDDIR := build/

build: clean check qms

qms: $(SCRIPTPATH)quick_map_server.py
	$(PY) $(SCRIPTPATH)quick_map_server.py -i icons/ -d datasource/ -b $(BLDDIR)

check: $(SCRIPTPATH)datasource_validate.py
	$(PY) $(SCRIPTPATH)datasource_validate.py -s schema.json -d datasource/

clean:
	rm -rf $(BLDDIR)*

$(BLDDIR):
	mkdir -p $(BLDDIR)
  