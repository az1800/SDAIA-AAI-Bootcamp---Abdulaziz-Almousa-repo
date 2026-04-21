---
title: "Sensitive Data"
format: html
---

In certain data-sensitive contexts (for instance, private health records or political or financial data) sharing a report that includes a sample would violate privacy constraints.

Examples: `salary`, `medical_diagnosis`, `political_contribution`, `account_balance`.

**Personal Identifiable Information** **(PII)** refers to any information that can be used to identify an individual. This includes but is not limited to, names, addresses, phone numbers, social security numbers, email addresses, and financial information.

Many countries and regions have stringent data protection regulations (such as GDPR, CCPA, or HIPAA) that require organizations to handle PII responsibly.

**Direct Identifiers** (PII): `name`, `email`, `national_id`, `phone_number`, `credit_card_number`.

**Quasi-Identifiers**: `zip_code`, `date_of_birth`, `gender`, `last_name`.

## Handle Sensitive Data

We want to ensure that individual records are protected while the dataset remains useful for analysis.

### A. Exclusion/Dropping

This method involves completely removing columns that contain sensitive information (like SSN or internal IDs) when they are not necessary for the specific analysis or report being generated. It is the most direct way to eliminate risk associated with a particular field.

```python
# Assuming 'df' is your DataFrame
df.drop(columns=['email', 'phone_number'], inplace=True)
```

### B. Masking

Masking replaces the sensitive values with non-informative characters (e.g., `*`) or a fixed placeholder string. This technique retains the column structure and alerts users that data was present but has been intentionally concealed.

```python
# Assuming 'df' has a 'phone_number' column
# show only the last 3 digits
df['phone_number'] = df['phone_number'].apply(lambda x: x[-3:])
```

### C. Hashing

Hashing transforms sensitive text or identifiers (such as `client_ID`) into a fixed-length, one-way cryptographic string. This allows for consistent tracking or merging of records without ever exposing the original, sensitive value. The original data cannot be recovered from the hash.

```python
import hashlib
import pandas as pd

# Use hashlib.sha256 for a strong, irreversible hash
df['client_id_hash'] = df['client_id'].astype(str).apply(
    lambda x: hashlib.sha256(x.encode()).hexdigest()
)
```

### D. Pseudonymization

Pseudonymization replaces identifiers with artificial, randomly generated identifiers (pseudonyms). This allows the data to be used for most analytical purposes, as the relationships between records are maintained, but the direct link to the real-world identity is broken.

```python
from faker import Faker
import pandas as pd

fake = Faker()
# Replace real names with realistic-sounding, fake names
df['name'] = df['name'].apply(lambda x: fake.name())
```

### E. Aggregation

Aggregation converts individual sensitive records into summary statistics (e.g., counts, means, sums) for specific groups. This is often done to meet reporting requirements where only non-identifying, overall trends are permitted, ensuring no single record is visible.

```python
# Grouping by a non-sensitive column ('age_group') and calculating the mean of 'salary'
df_agg = df.groupby('age_group')['salary'].mean().reset_index()
```

### F. Generalization

Generalization reduces the precision of quasi-identifiers (data that can, in combination, identify an individual) by replacing specific values with broader ranges or categories. Examples include replacing a precise age with an age range or a full ZIP code with a regional prefix.

```python
import pandas as pd

# Creating age groups instead of using exact age
bins = [0, 18, 35, 60, 100]
labels = ['0-18', '19-35', '36-60', '61+']
df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels)
```
