## README.md

ICD10CodeLookUp is a Python library that can be used to look up ICD10 Diagnosis Codes.

**Installation**

You can install ICD10CodeLookUp using pip:

```python
pip install ICD10CodeLookUp
```

#### Example usage
```python
import pandas as pd
import numpy as np
from ICD10CodeLookUp import DiagnosisCodeLookUp
```

#### Create an instance of the ICD10CodeLookUp class
```python
lookup = DiagnosisCodeLookUp()
```

##### Search for ICD10 diagnosis codes based on a keyword
```python
keyword = 'heart failure' # Let's use Heart failure as an example keyword
codes = lookup.search_by_keyword(keyword)
print("ICD10 diagnosis codes for keyword '{}': {}".format(keyword, codes))
```

##### Retrieve the ICD10 diagnosis code mapping as a dataframe
```python
df_mapping = lookup.get_mapping_dataframe(keyword)
print("\nICD10 diagnosis code Mapping (DataFrame):")
df_mapping
```

##### Retrieve the ICD10 diagnosis code mapping as a tuple list
```python
tuple_mapping = lookup.get_mapping_tuple_list(keyword)
print("\nICD10 diagnosis code Mapping Tuple List:")
tuple_mapping
```