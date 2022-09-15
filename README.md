
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Docker](https://img.shields.io/badge/docker-v20.10.2+-blue.svg)
![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![Task](https://img.shields.io/badge/task-KGQA-green.svg)
[![License](https://img.shields.io/badge/license-Apache2-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

The MuHeQA (Multiple and Heterogeneous Question-Answering) system creates natural language answers from natural language questions using knowledge base from both structured (KG) and unstructured (documents) data sources.


```bibtex
@inproceedings{paper2022,
  title={MuHeQA: Question Answering over Multiple and Heterogeneous Knowledge Bases},
  author={xxx},
  booktitle={xxx},
  url={https://xxx},
  year={2022}
}
```

## Preparation
1. Prepare a [Python 3](https://www.python.org/downloads/release/python-395/) environment and install the [Conda](https://docs.conda.io) framework.
2. Clone this repo:
	  ```
	  git clone https://github.com/librairy/MuHeQA.git
	  ```
3. Move into the root directory:
      ```
	  cd MuHeQA
	  ```
4. Create an environment (if it does not already exist):
      ````
      conda create --name .muheqa python=3.9
      ````
5. Activate the environment:
      ````
      conda activate .muheqa
      ````
6. Install requirements