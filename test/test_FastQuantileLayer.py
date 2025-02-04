import numpy as np 
from FastQuantileLayer import FastQuantileLayer

# PyTest testing infrastructure
import pytest

# Local testing infrastructure
from wrap import deploy_pickle 

################################################################################
## Test preparation

@pytest.fixture
def scaler_uniform():
  scaler_ = FastQuantileLayer()
  X = np.random.uniform (20,30,(1000, 10))
  scaler_.fit (X) 
  return scaler_

@pytest.fixture
def scaler_bool():
  scaler_ = FastQuantileLayer(output_distribution='normal')
  X = np.random.choice ([0., 1.],(1000, 10), [0.8, 0.2])
  scaler_.fit (X) 
  return scaler_

@pytest.fixture
def scaler_normal():
  scaler_ = FastQuantileLayer(output_distribution='normal')
  X = np.random.uniform (20,30,(1000, 10))
  scaler_.fit (X) 
  return scaler_


scalers = ['scaler_uniform', 'scaler_bool', 'scaler_normal']

################################################################################
## Real tests
@pytest.mark.parametrize ('scaler', scalers)
def test_forward (scaler, request):
  scaler = request.getfixturevalue(scaler)
  deployed = deploy_pickle("fastQL", scaler)
  xtest = np.random.uniform (20,30, 10)
  py = scaler.transform (xtest[None]).numpy()
  c  = deployed.transform (10, xtest)
  assert np.abs(py-c).max() < 1e-5
 

@pytest.mark.parametrize ('scaler', scalers)
def test_inverse (scaler, request):
  scaler = request.getfixturevalue(scaler)
  deployed = deploy_pickle("fastQL", scaler)
  xtest = np.random.uniform (0,1, 10)
  py = scaler.transform (xtest[None], inverse=True).numpy()
  c  = deployed.transform_inverse (10, xtest)
  assert np.abs(py-c).max() < 1e-5
 



