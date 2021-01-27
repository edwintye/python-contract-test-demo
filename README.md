# python-contract-test-demo

![CI](https://github.com/edwintye/python-contract-test-demo/workflows/CI/badge.svg) [![codecov](https://codecov.io/gh/edwintye/python-contract-test-demo/branch/main/graph/badge.svg?token=6IWt7qP6xM)](https://codecov.io/gh/edwintye/python-contract-test-demo)

### Creating a virtual env

Development should be done in a virtual environment; a conda environment file `conda.yml`
can be found in the project root and a new environment can be created via
```bash
conda env create -f conda.yaml
```

### Contract test

We put all the configuration in `api/dredd.yaml` which contains information on
how we would start the server as well as the location of the api spec and the
[hooks](https://dredd.org/en/latest/hooks/index.html).

As Dredd is based on Javascript, we have also put in [package.json](package.json)
to define the dependencies and how we would run the test.  Assuming that you have
npm/yarn installed, running the contract test locally is simply

```bash
yarn test
```

Running the test against another environment requires a little bit more effort, and
in general it is likely to be easier to use a docker image to run the contract test
instead during local development with a development server.

```bash
# have a development server running in the background
uvicorn demo.main:app --reload
# then run the contract test
docker run -it -v $(pwd):/mnt apiaryio/dredd:13.1.2 /mnt/api/open-api.yaml localhost:8000 --hooksfile=/mnt/api/hooks.js
```
