# Question Answering over Multiple and Heterogeneous Knowledge Bases

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Docker](https://img.shields.io/badge/docker-v20.10.2+-blue.svg)
![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![Task](https://img.shields.io/badge/task-KGQA-green.svg)
[![License](https://img.shields.io/badge/license-Apache2-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

The MuHeQA (Multiple and Heterogeneous Question-Answering) system creates natural language answers from natural language questions using knowledge base from both structured (KG) and unstructured (documents) data sources.

## Quick Start!

Install the `muheqa` package:
````python
pip install muheqa
````

Create a new connection to Wikidata, or DBpedia, or D4C (Drugs4Covid). *The first time it may take a few minutes to download the required models*:
````python
import muheqa.connector as mhqa

wikidata = mhqa.connect(wikidata=True)
````

And finally, make a question in natural language!:
````python
response = wikidata.query("Who is the father of Barack Obama")
print("Response:",response)
````


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
6. Download the [answer classifier](https://delicias.dia.fi.upm.es/nextcloud/index.php/s/Jp5FeoBn57c8k4M) and unzip into the root project directory. The folder `resources_dir/` is created.
      ````
      wget -O resources.zip https://delicias.dia.fi.upm.es/nextcloud/index.php/s/Jp5FeoBn57c8k4M/download
      unzip resources.zip
      ````
7. Install dependencies
      ````
      pip install -r requirements.txt
      ````

## M1 Environments (only for Apple's M1 devices)
1. Install TensorFlow dependencies
      ````
      conda install -c apple tensorflow-deps
      ````
2. Install base TensorFlow
      ````
      pip install tensorflow-macos
      ````
3. Install tensorflow-metal plugin
      ````
      pip install tensorflow-metal
      ````
