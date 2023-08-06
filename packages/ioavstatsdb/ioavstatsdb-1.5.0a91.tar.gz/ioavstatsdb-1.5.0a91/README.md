# IO-AVSTATS-DB - Aviation Event Statistics Database Software

The National Transportation Safety Board ([NTSB](https://www.ntsb.gov/Pages/home.aspx)) investigates all aviation accidents in the U.S. and makes the investigation results available on their [website](https://data.ntsb.gov/avdata) in Microsoft Access database files for public use. 
The NTSB provides data from 1982 through 2007 in the file **`Pre2008.zip`**. 
Data since 2008 are available first in the overall **`avail.zip`** file, which is updated monthly, and second with a "weekly" amendment file each month on the 1st, 8th, 15th, and 22nd, e.g. **`up22JUN.zip`**.

**IO-AVSTATS-DB** allows you to migrate Microsoft Access files to a PostgreSQL database.
After the data is uploaded based on the two files **`Pre2008.zip`** and **`avail.zip`**, the PostgreSQL can be kept up to date with the "weekly" amendment files.

To validate and supplement the NTSB data in certain aspects, the following data collections are additionally used: 

- [**AVIATION OCCURRENCE CATEGORIES**](https://www.ntsb.gov/safety/data/Documents/datafiles/OccurrenceCategoryDefinitions.pdf)
- [**FAA Airports**](https://adds-faa.opendata.arcgis.com/datasets/faa::airports-1/explore?location=0.158824%2C-1.633886%2C2.00)
- [**FAA Runways**](https://adds-faa.opendata.arcgis.com/datasets/faa::runways/explore?location=0.059024%2C-1.628764%2C2.00)
- [**geodatos**](https://www.geodatos.net/en)
- [**National Plan of Integrated Airport Systems (NPIAS)**](https://www.faa.gov/airports/planning_capacity/npias/current)
- [**opendatasoft**](https://www.opendatasoft.com/?hsLang=en)
- [**simplemaps**](https://simplemaps.com/)
- [**United States Zip Codes.org**](https://www.unitedstateszipcodes.org/)

The functionality includes the following tasks:

| Task                                                   | Code        | 
|--------------------------------------------------------|-------------|
| Cleansing PostgreSQL data                              | **`c_p_d`** |
| Complete processing of a modifying MS Access file      | **`u_p_d`** |
| Correct decimal US latitudes and longitudes            | **`c_l_l`** |
| Create the PostgreSQL database schema                  | **`c_d_s`** |
| Find the nearest airports                              | **`f_n_a`** |
| Load NTSB MS Access database data into PostgreSQL      | **`l_n_a`** |
| Load ZIP Code Database data into PostgreSQL            | **`l_z_d`** |
| Load airport data into PostgreSQL                      | **`l_a_p`** |
| Load aviation occurrence categories into PostgreSQL    | **`a_o_c`** |
| Load country and state data into PostgreSQL            | **`l_c_s`** |
| Load data from a correction file into PostgreSQL       | **`l_c_d`** |
| Load sequence of events data into PostgreSQL           | **`l_s_e`** |
| Load simplemaps data into PostgreSQL                   | **`l_s_d`** |
| Refresh the PostgreSQL database schema                 | **`r_d_s`** |
| Update the PostgreSQL database schema                  | **`u_d_s`** |
| Verify selected NTSB data                              | **`v_n_d`** |

All processing tasks can be performed using the **`run_io_avstats`** shell script.

## Documentation

Since this is a private repository, the complete documentaion is only available in a local version of the repository in the file directory **`site`**. 
You just have to open the file **`site/index.html`** with a web browser.

## Directory and File Structure of this Repository

### 1. Directories

| Directory         | Content                                                    |
|-------------------|------------------------------------------------------------|
| .github/workflows | **[GitHub Action](https://github.com/actions)** workflows. |
| data              | Application data related files.                            |
| dist              | Installable versions of the **IO-AVSTATS-DB** software.    |
| docs              | Documentation files.                                       |
| resources         | Selected manuals and software.                             |
| scripts           | Scripts supporting Ubuntu and Windows.                     |
| site              | Documentation as static HTML pages.                        |
| src               | Python script files.                                       |
| tests             | Scripts and data for **pytest**.                           |

### 2. Files

| File                      | Functionality                                                 |
|---------------------------|---------------------------------------------------------------|
| .gitignore                | Configuration of files and folders to be ignored.             |
| .pylintrc                 | **pylint** configuration file.                                |
| .settings.io_avstats.toml | Configuration data - secrets.                                 |
| LICENSE.md                | Text of the licence terms.                                    |
| logging_cfg.yaml          | Configuration of the Logger functionality.                    |
| Makefile                  | Tasks to be executed with the **`make`** command.             |
| mkdocs.yml                | Configuration file for **MkDocs**.                            |
| Pipfile                   | Definition of the Python package requirements.                |
| Pipfile.lock              | Definition of the specific versions of the Python packages.   |
| pyproject.toml            | Optional configuration data for the software quality tools.   |
| README.md                 | This file.                                                    |
| run_io_avstats            | Main script for using the functionality of **IO-AVSTATS-DB**. |
| settings.io_avstats.toml  | Configuration data.                                           |
| setup.cfg                 | Optional configuration data for **flake8**.                   |
