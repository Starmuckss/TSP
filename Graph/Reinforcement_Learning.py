# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 10:53:14 2022

@author: HP
"""
from scipy.spatial.distance import cdist
import numpy as np

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import time
from tqdm import tqdm_notebook

from delivery import *

env = DeliveryEnvironment(n_stops = 10)