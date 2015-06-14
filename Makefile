PY=python
SCRIPTPATH=scripts/
BLDDIR := build/

build: qms

test: qms qmstest

qms: clean check quick_map_server

qmstest:
	rm -rf ~/.qgis2/python/plugins/quick_map_services/data_sources
	rm -rf ~/.qgis2/python/plugins/quick_map_services/groups
	cp -rf $(BLDDIR)/qms/* ~/.qgis2/python/plugins/quick_map_services/

quick_map_server: $(SCRIPTPATH)quick_map_server.py
	$(PY) $(SCRIPTPATH)quick_map_server.py -i icons/ -d datasource/ -b $(BLDDIR)/qms/

check: $(SCRIPTPATH)datasource_validate.py
	$(PY) $(SCRIPTPATH)datasource_validate.py -s schema.json -d datasource/

clean:
	rm -rf $(BLDDIR)*

$(BLDDIR):
	mkdir -p $(BLDDIR)
  