<p align=center><img src=_src/assets/income.png height=627 weight=1247><p>

# <h1 align=center> **Income Credit Score System with Machine Learning** </h1>

# Introduction

This is a ready to use income score project using machine learning techniques.<br> 
This project has used DVC with GCP and GitHub action to create a complete autonomous training and deployment system.<br>

<p align=center><img src=_src/assets/tech.png><p>

# Project Overview

The main objective of the project is to provide clients with a useful tool to qualify profiles and 
evaluate the repayment ability of applicants for all types of personal loans and credits. The income 
score will be built using individual information from the profile, as well as external data 
(demographic data, national surveys/household surveys, among other datasets) that refer to your 
environment. This combination of information will allow obtaining a clearer and more precise image 
of the financial situation of each person. To give customers a better understanding of each 
profile's ability to pay, alternate credit scores are used. Customers will be able to issue credit 
in an informed and data-driven manner by using the score as a quantitative indicator.<br>
<br>
The main advantage of the income score built in this project lies in the combination of individual 
profile information and external data referring to its environment. By considering factors such as 
income, job seniority, number of jobs in recent years, age, state/province, income growth, 
education, type and behavior of the industry, and social status of the population, a more complete 
and comprehensive perspective is obtained. accurate profile of the applicant. Some of these 
variables are obtained directly from the MOX datasets such as the specific variables of the profile, 
the other variables about their environment will be obtained from public databases, open government 
data and surveys.<br>
<br>
The deliverable of the project is to create a score that gathers the different data around the 
requested profile and immediately offers a balanced metric for easy classification of the profile.

# Frontend

The following picture shows a basic but complete frontend visualization of the project made with **Streamlit**.

<p align=center><img src=_src/assets/front.png><p>

# Project architecture

The following picture shows the architecture and the main used technologies in this project.

<p align=center><img src=_src/assets/architecture.png><p>

# Repository content

- **.dvc/**: DVC configuration files.
- **.github/workflows/**: Github Actions.
- **.streamlit/**: Frontend configurations.
- **api/**: API development.
- **business_rules/**: JSON file with business rules.
- **dataset/**: Dataset files.
- **frontend/**: Frontend development.
- **model/**: machine learning models files.
- **notebooks/**: Notebooks file with etl and machine learning.
- **src/**: Training scripts files.
- **testing/**: API test files.
- **utilities/**: Utils functions.
- **…**: Miscellaneous project files.

## The main tasks that are executed in the pipeline

- Cloning the working main branch.
- Creation of a virtual environment.
- Dependencies install (requirements.txt).
- Environment variables configuration to be able to access the GCP storage.
- Acquisition of the models and datasets stored in the GCP storage using the DVC tool.
- Execution of the ETL script and the Machine Learning script which will generate new models and new datasets.
- Storage of the new models and datasets created in the GCP storage using the DVC tool.
- Update of the git repository with the new files that contain the reference to the previously created models and datasets.
- Publication of the most important metrics and sending information to the email address configured to monitor the status of the model.


<p align=center><img src=_src/assets/tasks.png><p>


# Section 1

## GCP Storage Configuration

- Create a new project.

<p align=center><img src=_src/assets/new_project.png><p>

- Go to APIs and Services -> Credentials.

<p align=center><img src=_src/assets/api_service.png><p>

- Create a new Service Account credentials.

<p align=center><img src=_src/assets/create_credential.png><p>

- Set a name that will be used by DVC forward.
- Permission asigment:  Storage -> Cloud Storage -> Storage Admin
- Go to the storage created and download the JSON credential.

<p align=center><img src=_src/assets/storage.png><p>
<p align=center><img src=_src/assets/storage_key.png><p>
<p align=center><img src=_src/assets/storage_key_json.png><p>

- Store the key in the project.
- Set the environment variable

```
export GOOGLE_APPLICATION_CREDENTIALS=$(realpath <credential-file>.json)
```

- Check the environment variable:

```
echo $GOOGLE_APPLICATION_CREDENTIALS
```

[Video Section 1](https://drive.google.com/file/d/1sbK0NhaJPixd95YyEI_jdWscAvkKP3rT/view?usp=sharing)

# Section 2

## Create a Bucket to store the serialized data (datasets and models).

- Go to Cloud Storage -> Bucket -> Create

<p align=center><img src=_src/assets/create_bucket.png><p>
<p align=center><img src=_src/assets/create_bucket_1.png><p>

- Set the name as follow `model-and-dataset-tracker`.
- Other fields by default.
- Create a folder for dataset and for model with the following names:
  - `dataset`
  - `model`

>Note: It is important to use the same names, otherwise it will need to change the .dvc/config file.

[Video Section 2](https://drive.google.com/file/d/1lq9G0eI5cP-gKNjilLhXWyDfXHorkxN8/view?usp=sharing)

# Section 3

## Create GCP credentials to deploy with Github Actions

- Go to APIs and Services in the left tab -> Credentials

<p align=center><img src=_src/assets/service.png><p>

- Create credentials -> Service Account

<p align=center><img src=_src/assets/credentials.png><p>

- Set a name and continue.
- Set the following roles:
  - Cloud Storage -> Storage admin (Cloud storage control)
  - Cloud Run -> Cloud Run admin (Cloud run resource control)
  - Artifact Registry -> Artifact registry admin (create and admin repositories)
  - Service Account -> Service Account user (To deploy in cloud run)
- Select Ready

<p align=center><img src=_src/assets/ready.png><p>

- Once the account is created go to the account and add a JSON key.

<p align=center><img src=_src/assets/key.png><p>

- Copy the JSON file inside the project an in a shell console run the following command:

```
base64 <file-name>.json
```
- Copy the output
- Go to Github -> Setting -> Secrets and Variables -> Actions -> New Repository Secret

<p align=center><img src=_src/assets/secret.png><p>

- Create SERVICE_ACCOUNT_KEY secrete name and paste the `base64 <file-name>.json` output.

[Video Section 3](https://drive.google.com/file/d/1rmDh7hRnXPijSRR7yUBLrY9OLR9cUiHE/view?usp=sharing)

# Section 4

## Create a Cloud Run Service for the API

- Go to Cloud Run 

<p align=center><img src=_src/assets/cloud_run.png><p>

- Create Service

<p align=center><img src=_src/assets/create_service_cloud_run.png><p>

- Click in Select -> Container Registry -> Demo Container -> Hello -> Ok

<p align=center><img src=_src/assets/select.png><p>

- Set Service Name
- Set Region `us-central1 (Iowa)`
- Authentication -> Allow unauthenticated invocations
- Set Minimun Instance Number = 1
- Set Maximun Instance Number = 10 or greater
- Select Containers, Net tools, Security

<p align=center><img src=_src/assets/containers.png><p>

- Container Port = 8000
- Memory = 1Gb or greater
- Maximum number of concurrent requests per instance = 10 or greater
- Create


[Video Section 4](https://drive.google.com/file/d/1lul17xlwB0mtt9JGaaUvNEChT_KYg2rR/view?usp=sharing)

## Create a Cloud Run Service for the Frontend App

- Repeat the previous steps but set the Container Port to 8080


# Section 5

## Configure Github with secrets for Cloud Services

- Open Github and Add new secrets
- Go to Settings -> Secretes and Variables -> New Repository Secret

<p align=center><img src=_src/assets/secret.png><p>

The following secrets can be found in the Cloud Run Services created in the previous steps.

- Add REGION

<p align=center><img src=_src/assets/region.png><p>

>Note: The region can be found as the following picture shows

<p align=center><img src=_src/assets/region_gcp.png><p>

>Note: As both services created have the same region, one REGION secret is enough.

- Add REGISTRY_NAME 
- Add REGISTRY_NAME_FRONT
- Add PROJECT_ID

The REGISTRY_NAME and REGISTRY_NAME_FRONT can be created as follow:

gcr.io/<PROJECT_ID>/<NAME_REG>

Where NAME_REG is a name that we pick and PROJECT_ID can be found as follow.

<p align=center><img src=_src/assets/project_id.png><p>

Example

```
REGISTRY_NAME = gcr.io/mox-storage-project-test/scoring-ml
REGISTRY_NAME_FRONT = gcr.io/mox-storage-project-test/scoring-ml-frontend
PROJECT_ID = mox-storage-project-test
```

- Add SERVICE_NAME
- Add SERVICE_NAME_FRONT

>Note: The SERVICE_NAME and SERVICE_NAME_FRONT can be found as the following picture shows

<p align=center><img src=_src/assets/service_name.png><p>


At the end of these steps, the following secrets must be created in order to get the app working

<p align=center><img src=_src/assets/all_secrets.png><p>


[Video Section 5](https://drive.google.com/file/d/1M-9_j5osQd3xqZBFY-YGD0JhJvDTljvv/view?usp=sharing)


## Configure Github with secrets for MongoDB access

In order to preserve MOX privacy, it has created an environment variable with the MongoDB URL.<br>
Create a secret with the following name:

- URL_DATABASE

Add the URL to get access to the dataset to create and train models.


## Get URL from API service in the frontend

In order to set the URL to achieve the API from de Frontend you should configure the `config.json` file which is located in `frontend` folder. The file content is the following:

```
{
    "frontend-service-name": SERVICE_NAME_FRONT,
    "api-service-name": SERVICE_NAME
}
```

Where `SERVICE_NAME_FRONT` and `SERVICE_NAME` are the same that have been set in the previous sub-section.

Example

```
{
    "frontend-service-name": "scoring-front-service",
    "api-service-name": "scoring-service"
}
```

# Section 6

## Continuous Training Configuration

The continuous training was set to be automaticaly by Github Actions in the `.github/workflows/continuous_training.yaml` file, and it will be done everytime the cloud deployment is triggered or/and every day at midnight, set by a cron job.<br>
To configure email report please configure the `.github/workflows/continuous_training.yaml` file with your own email as is shown in the picture below:


[Video Section 6](https://drive.google.com/file/d/1TD3LpNXcUTqBZyKhS64D6kqVlyRC_Jg2/view?usp=sharing)

# Section 7

## Cloud Deployment

Once the Cloud is configured, you can push the content of your local repository to the remote.
The cloud deployment was set to be automaticaly by Github Actions in the `.github/workflows/ci_cd.yaml` file, and it will be done everytime a `git push` command is excecuted into the `main` branch.<br>
The path for the frontend service can be found in the Cloud Run Service. For this deployment run the following [link](https://scoring-front-service-tq7rapbbua-uc.a.run.app/).<br>
The path for the API service can be found in the Cloud Run Service. For this deployment run the following [link](https://scoring-service-tq7rapbbua-uc.a.run.app/).<br>
To check the status of the Github Actions, you can go to tha Actions tab in your repository. The first push you make you will find that the following workflows fail:
- Testing API
- Continuous Integration - Continuous Deployment 
- Continuous Training

<p align=center><img src=_src/assets/fail.png><p>

This is because the first push the models do not exist in the remote bucket, but after `Continuous Training` excecution, models will be created and a new `Continuous Integration - Continuous Deployment` workflow will be launched. After this workflow finish all services will be loaded correctly.

<p align=center><img src=_src/assets/email_git.png><p>


[Video Section 7](https://drive.google.com/file/d/1HylTKDZLisRKOieEZ6Z_w4USoTlojOQu/view?usp=sharing)


# Section 8

## Local Deployment

For this deployment it is required python 3.10 version. 
Check python version 

```
python3 --version
```

To install python 3.10 please follow the steps on the following [link](https://computingforgeeks.com/how-to-install-python-on-ubuntu-linux-system/?expand_article=1)

Inside the project folder, create a virtual environment and install the requirements librariies:

```
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
python3 -m pip install -r src/requirements.txt
```

Set the environment variable to reach the database as follow:

```
export URL_DATABASE='<mongodb_url>'
echo $URL_DATABASE
```

For these steps the environment variable must be set as follow and models must be already in the `model` folder and dataset in the `dataset` folder:

```
export GOOGLE_APPLICATION_CREDENTIALS=$(realpath <credential-file>.json)
```

Where `<credential-file>.json` was downloaded in the **GCP Storage Configuration** section

Check the environment variable:

```
echo $GOOGLE_APPLICATION_CREDENTIALS
```

If models `.pkl` do not exist in the model folder neither `data_prueba_limpia.csv` in the dataset folder run the following command to create then:

```
dvc repro -f prepare
dvc repro -f training
```

If models and `data_prueba_limpia.csv` exists, run 

```
dvc repro -f
```

This will run the preparation and training methods.

>Note: In case dvc command is not recognized, it can be used `python -m dvc repro -f`. You should make sure that the python version running inside the file `dvc.yaml` is the 3.10, otherwise the command will thrown an exception. To check python version for dvc command, in the `dvc.yaml` file create an stage with `python --version` command or replace the existed stage and run the dvc command explained before.

Run the docker compose file to deploy the project:

```
docker compose up -d --build
```

The frontend deployment can be found in the following browser path:

```
<IP ADDRESS>:8080
```

The API deployment can be found in the following browser path:

```
<IP ADDRESS>:8000
```

>Note: If the models and datasets are not in the respective forlder the deployment will fail. Follow the section 10 to create and store the models and datasets.


# Section 9

## DVC (Data Version Control) Initialization

- Install dvc and dvc-gs dependencies

```
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
dvc init
```
- Once the JSON credential of the previous steps is downloaded and copied into the porject, set the environment variable as follow:

```
export GOOGLE_APPLICATION_CREDENTIALS=$(realpath <credential-file>.json)
```

- Check the environment variable:

```
echo $GOOGLE_APPLICATION_CREDENTIALS
```

- Connect DVC with the GCP remote bucket

```
dvc remote add <bucket-reference> gs://<bucket-name>/<folder>
```
bucket-reference: Name to refer to the storage, this name will be stored in `.dvc/config` file.
bucket-name: Use the same bucket name sets in the `GCP Storage Configuration` step. 
folder: Folder created in the bucket to storage elements.


Example:

For the dataset folder we can use:

```
dvc remote add dataset-track gs://model-and-dataset-tracker/dataset
```

For the model folder we can use:

```
dvc remote add model-track gs://model-and-dataset-tracker/model
```

In order to create a local or manual deployment we can storage the CSV (datasets) and PKL (models) manually (in case files do not exist read the next section). To do so

```
dvc add <file-name>
dvc push <file-name> -r <bucket-reference>
```
Where <bucket-reference> is stored in `.dvc/config` file.

Example:

```
dvc add model/model.pkl
dvc push model/model.pkl -r model-track
```


# Section 10

### CVS and Model creation

In case the `PKL` files in the `model` folder and `data_prueba_limpia.csv` file in the `dataset` folder do not exist, run the following command to create them:

```
dvc repro -f
```

This command will excecute the `dvc.yaml` and it will run the `notebooks/etl_process.ipynb` to create the `data_prueba_limpia.csv` file. After the excecution it will run the `notebooks/models.ipynb` to create the machine learning models.

Once those file are created can be storage and tracked with DVC following the steps in the ***DVC (Data Version Control) Initialization** section.


# Section 11

## API deployment

In the [link](https://scoring-service-tq7rapbbua-uc.a.run.app/#/default/make_model_prediction_v1_prediction_post) for the API you can find the information about the endpoint and the input and outpud data.<br>

### Endpoint 

```
/v1/prediction
```

### Input JSON schema: 

```
{
  "ingreso": 0,
  "antiguedad_laboral_meses": 0,
  "tiempo_desempleado": 0,
  "trabajos_ultimos_5": 0,
  "semanasCotizadas": 0,
  "edad": 0,
  "crecimiento_ingreso": 0,
  "lugar_actual": 0
}
```

### Input data type:

```
ingreso: float
antiguedad_laboral_meses: int
tiempo_desempleado: int
trabajos_ultimos_5: int
semanasCotizadas: int
edad: int
crecimiento_ingreso: float
lugar_actual: int
```

### Output JSON schema: 

```
{
  "scoring": 323.75,
  "cluster": "C"
}
```
### Output data type:

```
scoring: float
cluster: str
```

# License

This project is licensed under the GPL-2.0 license.