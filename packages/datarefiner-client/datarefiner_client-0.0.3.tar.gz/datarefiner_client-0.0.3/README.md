**Readme**

DataRefiner Client Library is a Python API toolkit designed to seamlessly connect your Python code with the DataRefiner platform, enabling convenient access and interaction.

**Website**: [https://datarefiner.com](https://datarefiner.com)

### What functions this library support? ###

* Login using API key
* Perform Supervised labelling (predict cluster labels and groups from trained toplogical project)

### Usage example: 
###

```
import pandas as pd
from datarefiner_client import DataRefinerClient

# Login using API key
client = DataRefinerClient(
    token='datarefiner_token',
    base_url='https://app.datarefiner.com',
)
client.me()

# Loading new data from CSV file
project_id = 2698269341
df = pd.read_csv("./data.csv")

# Performig prediction for new data
clusters_df, groups_df = client.supervised_labeling(project_id=project_id, df=df)
```
