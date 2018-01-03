<p align="center">
  <a href="https://github.com/sylvinite/microSALT">
    <img width="1000" height="250" src="artwork/microsalt.jpg"/>
  </a>
</p>

microbial Sequence Analysis and Loci-based Typing pipeline

## Requirements
* Python 3.6
* MySQL

* BLAST
* CutAdapt
* SpaDES

* Genologics, `https://github.com/SciLifeLab/genologics.git`

## Configuration
### Flask/Database configuration
Rename the configuration file under folder `instance` to `sqlalchemy_config.py` and modify the line `SQLALCHEMY_DATABASE_URI` to correctly point to your database. For production purposes, set the `DEBUG` flag to False.

### Paths file
Review `microSALT/paths.yml` to accurately represent the file paths and sbatch headers required by your system.

### LIMS
Create `$HOME/.genologicsrc` with the following formatting:
```
[genologics]
BASEURI=https://yourlims.example.com:8443
USERNAME=your_username
PASSWORD=your_password
[logging]
MAIN_LOG=/home/glsai/your_main_log_file
```

Additionally `ConfigParser` in `config.py` needs to be replaced with `configparser` for python3 support.

## Usage
* Use the `rename` function on the folder of your input fastq files
* Use the `create` function to generate sbatch job(s) defined under `folders['results']`. Manually start them via the `concatinated.sh` script.
* After the jobs have been finished. Use the `scrape` function to upload parsed results to the SQL backend.
* Use the `view` function to start a flask instance to view the results. Point your browser at `http://127.0.0.1:5000/`
* Navigate to your run, and print the results to PDF format if necessary.
