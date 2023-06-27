# sinka97-deployment
My portfolio website sinka97, containing some personal projects as django apps.
Live deployment can be viewed [here](https://sinka97.com/).

## [Portfolio Website](https://sinka97.com/portfolio/)
A personal website containing information about me and my porfolio.
Built with Django and Bootstrap.

## [Totolyzer](https://sinka97.com/totolyzer/)
A data engineering/data visualisation project using data from Singapore Pools Toto Results.
Currently a work in progress, the project is aimed at honing my skills.
* Seeding Postgresql database using csv data for historical Toto results (Completed).
* Data visualisation (Frequency, Co-occurence, Aggregation) of Toto Results (Completed).
* Daily fetching of data from Singapore Pools website to retrieve the latest Toto results and store into Postgres database in AWS RDS (In Progress).
* Seeding Data into Neo4j database using csv data for historical Toto results (In Progress).
* Daily fetching of data from Public Weather APIs and storing into Postgres database & Neo4j database (In Progress).
* Data visualisation (Relationships) of Toto Results & Weather & Date (In Progress).

### Tech Stack
* Python
  * Django
  * Pandas
  * Dash
  * Plotly
  * Gunicorn
* PostgreSQL
* Docker
* Nginx

### Data
* Seed historical data from https://en.lottolyzer.com/history/singapore/toto
* Subsequent fetching of Toto Results from https://www.singaporepools.com.sg/en/product/Pages/toto_results.aspx
* Weather data from https://data.gov.sg/dataset/realtime-weather-readings