import pandas as pd
import numpy as np


def create_sample():
    df = pd.read_csv("sample.csv")
    print(df)


create_sample()
