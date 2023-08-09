========
TDS2STAC
========

.. image:: https://codebase.helmholtz.cloud/cat4kit/tds2stac/-/raw/main/tds2stac-logo.png




=========

.. image:: https://img.shields.io/pypi/v/tds2stac.svg
        :target: https://pypi.python.org/pypi/tds2stac

.. image:: https://readthedocs.org/projects/tds2stac/badge/?version=latest
        :target: https://tds2stac.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



STAC specification is a method of exposing spatial and temporal data collections in a standardized manner. Specifically, the `SpatioTemporal Asset Catalog (STAC) <https://stacspec.org/en>`_ specification describes and catalogs spatiotemporal assets using a common structure. 
This package creates STAC metadata by harvesting dataset details from the `Thredds <https://www.unidata.ucar.edu/software/tds/>`_ data server. After creating STAC Catalogs, Collections, and Items, it imports them into `pgSTAC <https://stac-utils.github.io/pgstac/pgstac/>`_ and `STAC-FastAPI <https://stac-utils.github.io/stac-fastapi/>`_.

* Free software: EUPL-1.2
* Documentation: https://tds2stac.readthedocs.io.


Installation from PyPi
------------------------
.. code:: bash

   pip install tds2stac

Installation for development
--------------------------------
.. code:: bash

   git clone https://codebase.helmholtz.cloud/cat4kit/tds2stac.git
   cd tds2stac
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements_dev.txt


Installing using Docker
------------------------

For runnig by docker use `this <https://codebase.helmholtz.cloud/cat4kit/tds2stac-docker>`_ repository.


Usage
----------------
 
Use case:

You can use the following template for creating STAC catalog from the TDS web service for your project.

You can change configuration of PgSTAC in `config_pgstac <./tds2stac/config_pgstac.py>`_

.. code:: python

   from tds2stac.tds2stac import Converter

   converter = Converter("http://172.27.80.119:8088/thredds/catalog/regclim/raster/global/era5/sfc/catalog.html",
                        stac=True, stac_dir="/path/to/save/stac/catalogs/",
                        stac_id = "sample",
                        stac_description = "sample",
                        web_service = "iso" or "ncml",
                        datetime_filter=["2020-02-18T00:00:00.000Z","2020-02-22T00:00:00.000Z"],
                        stac_catalog_dynamic = True)

   output:

        Start Scanning datasets of http://172.27.80.119:8088/thredds/catalog/regclim/raster/global/era5/sfc/catalog.xml
        |__ http://172.27.80.119:8088/thredds/catalog/regclim/raster/global/era5/sfc/catalog.xml |  Number of branches:  5
        |_______ http://172.27.80.119:8088/thredds/catalog/regclim/raster/global/era5/sfc/static/catalog.xml |  Number of data:  1
        |_______ http://172.27.80.119:8088/thredds/catalog/regclim/raster/global/era5/sfc/monthly/catalog.xml |  Number of data:  246
        |_______ http://172.27.80.119:8088/thredds/catalog/regclim/raster/global/era5/sfc/daily/catalog.xml |  Number of data:  360
        |_______ http://172.27.80.119:8088/thredds/catalog/regclim/raster/global/era5/sfc/climatology/catalog.xml |  Number of data:  7
        |_______ http://172.27.80.119:8088/thredds/catalog/regclim/raster/global/era5/sfc/aggregated/catalog.xml |  Number of data:  1
        615 data are going to be set as items
        5 data are going to be set as items
        Start processing:  http://172.27.80.119:8088/thredds/catalog/regclim/raster/global/era5/sfc/static/catalog.xml
        5 / 5 STAC catalogs are created
        1 / 615 STAC items are connected to the related catalog
        100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 12.70it/s]
        Start processing:  http://172.27.80.119:8088/thredds/catalog/regclim/raster/global/era5/sfc/monthly/catalog.xml
        5 / 5 STAC catalogs are created
        247 / 615 STAC items are connected to the related catalog
        100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 246/246 [00:47<00:00,  5.17it/s]
        Start processing:  http://172.27.80.119:8088/thredds/catalog/regclim/raster/global/era5/sfc/daily/catalog.xml
        5 / 5 STAC catalogs are created
        607 / 615 STAC items are connected to the related catalog
        100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 360/360 [01:12<00:00,  4.95it/s]
        Start processing:  http://172.27.80.119:8088/thredds/catalog/regclim/raster/global/era5/sfc/climatology/catalog.xml
        5 / 5 STAC catalogs are created
        614 / 615 STAC items are connected to the related catalog
        100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00,  7.52it/s]
        Start processing:  http://172.27.80.119:8088/thredds/catalog/regclim/raster/global/era5/sfc/aggregated/catalog.xml
        5 / 5 STAC catalogs are created
        615 / 615 STAC items are connected to the related catalog
        100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:23<00:00, 23.93s/it]
        Start processing:  http://172.27.80.119:8088/thredds/catalog/regclim/raster/global/era5/sfc/catalog.xml
        5 / 5 STAC catalogs are created
        615 / 615 STAC items are connected to the related catalog
        0it [00:00, ?it/s]
        ./catalog_regclim_raster_global_era5_sfc_static/collection.json
        |____ ./era5_sfc_0.25_static_ERA5_Landsea_mask.nc/era5_sfc_0.25_static_ERA5_Landsea_mask.nc.json
        ./catalog_regclim_raster_global_era5_sfc_monthly/collection.json
        |____ ./era5_sfc_0.25_monthly_ERA5_monthly_ws10_2018.nc/era5_sfc_0.25_monthly_ERA5_monthly_ws10_2018.nc.json
        .
        .
        .
        |____ ./era5_sfc_0.25_daily_ERA5_daily_sp_1982.nc/era5_sfc_0.25_daily_ERA5_daily_sp_1982.nc.json
        |____ ./era5_sfc_0.25_daily_ERA5_daily_sp_1981.nc/era5_sfc_0.25_daily_ERA5_daily_sp_1981.nc.json
        ./catalog_regclim_raster_global_era5_sfc_climatology/collection.json
        |____ ./era5_sfc_0.25_climatology_ERA5_climatology_ws10_1981_2016.nc/era5_sfc_0.25_climatology_ERA5_climatology_ws10_1981_2016.nc.json
        |____ ./era5_sfc_0.25_climatology_ERA5_climatology_tp_1981_2016.nc/era5_sfc_0.25_climatology_ERA5_climatology_tp_1981_2016.nc.json
        |____ ./era5_sfc_0.25_climatology_ERA5_climatology_t2min_1981_2016.nc/era5_sfc_0.25_climatology_ERA5_climatology_t2min_1981_2016.nc.json
        ./catalog_regclim_raster_global_era5_sfc_aggregated/collection.json
        |____ ./era5_sfc_0.25_aggregated_ERA5_daily_tp_1979_2018.nc/era5_sfc_0.25_aggregated_ERA5_daily_tp_1979_2018.nc.json
        STAC Catalog has been created!

Copyright
---------
Copyright © 2023 Karlsruher Institut für Technologie

Licensed under the EUPL-1.2-or-later

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the EUPL-1.2 license for more details.

You should have received a copy of the EUPL-1.2 license along with this
program. If not, see https://www.eupl.eu/.
