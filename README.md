<p align="center">
  <a href="" rel="noopener">
 <img width=400px height=200px src="docs\Public_key_encryption_keys.svg.png" alt="Project logo"></a>
</p>

<h1 align="center">Organizing Records for Retrieval in Multi-Dimensional Range Searchable Encryption</h1>


## 📝 Table of Contents

- [About](#about)
- [Dependencies](#dependencies)
- [Running the Experiments](#experiments)


##  About <a name = "about"></a>
The project involves conducting experiments related to the paper "Organizing Records for Retrieval in Multi-Dimensional Range Searchable Encryption".

## 🏁 Dependencies <a name = "dependencies"></a>

In order to run the code, you must have Python 3.10.12 or newer versions installed. You can find the installation source [here][def].<br />
The `req.txt` file located in the main directory lists all the required dependencies for executing the project. You can install these dependencies by using the command `pip install -r req.txt`.

## 🏁 Running the Experiments <a name = "experiments"></a>


### Configurations
You can change the configurations for the experiments in the dsconfig.py file based on the following parameters:<br />
    `sample_num = 1000`<br />
    `datadim = [Number of dimensions,D1_size, D2_size, D3_size, D4_size]`<br />
    `slabdim = [4, 4, 4, 4]--> For slab-based shuffling`<br />
    `slab_size = 256 --> For row-based shuffling`<br />
The first element in datadim is the number of dimensions, and the following elements are the dimensions' sizes. <br />
sample_num is the number of sample random queries of the query shape.

### Generating Synthetic dataset
Before running the query experiments we should generate synthetic datasets based on the desired configurations. You can set your desired dataset settings as described in the configurations sections in the construction.py file<br />
Then, create a folder named 'sample_data' in the project's root directory.<br />
Run the `python3 src/construction.py` to generate all the mappings, encryption, indexing, and the synthetic dataset.

### Isotropic queries
Run the command `python3 src/isoqreport.py`<br />

### Bisected Anisotropic queries
Run the command `python3 src/baqreport.py`<br />

### Gradual Anisotropic queries
Run the command `python3 src/gaqreport.py`<br />

### Outlier queries
Run the command `python3 src/oaqreport.py -ot max` for max outlier queries<br />
Run the command `python3 src/oaqreport.py -ot min` for min outlier queries<br />

### reports:
The generated reports in .csv format will be stored in `sample_data/` folder. Remove the existing .csv report before running each experiment to have a clean report.





[def]: https://www.python.org/downloads/source/
