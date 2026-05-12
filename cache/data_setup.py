import pandas as pd
from pandas import DataFrame as dm
from pandas import read_excel as de
from pandas import read_csv as dc
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

import polars as pl
pl.Config.set_tbl_rows(30).set_tbl_cols(30).set_fmt_str_lengths(60)
pa = pl.nth(0)
pas = pa.str
pz = pl.nth(-1)
pzs = pl.last().str
pb = pl.nth(1)
pal = pl.all()
pall = pl.all().list
pals = pl.all().str
Pli = pl.Int64
CL = pl.lit

import numpy as np

df = None
df1 = None
df2 = None
dl = None
dl1 = None
dl2 = None

import random as rd
rd.seed(42)
import re

connMy = "mysql://shuai260103:MT4LxRjSNPsj9vFt@mysql6.sqlpub.com:3311/urlmysql"
dfgit = pd.read_csv("https://raw.githubusercontent.com/panhuangshuang-cyber/grok_python/main/0511.csv")
dfgit
