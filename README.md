# dfcleaner

> dataframe cleaning package

This package contains helper methods to clean pandas dataframe quickly and therefore simplifying the data cleaning process

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

OS X & Linux:

```sh
pip3 install dfcleaner
```

Windows:

```sh
pip install dfcleaner
```

## Usage example

```Python
import pandas as pd
from dfcleaner import cleaner

cleaner.ENABLE_LOGGING = True
cleaner.LOG_DIR = './logs'

df = pd.read_csv('some_filename.csv')

df = cleaner.sanitize_column_names(df)
conversion_dict = cleaner.suggest_conversion_dict(df)
df = cleaner.preprocess(df,
                        column_dtype_conversion_dictionary = conversion_dict,
                        std_coeff = 1.5,
                        fill_na_method = 'median',
                        label_col = None)
```

## Development setup

```sh
pip3 install -r requirements.txt
```

Windows:

```sh
pip install -r requirements.txt
```

## Meta

M. Zahash – zahash.z@gmail.com

Distributed under the MIT license. See `LICENSE` for more information.

[https://github.com/zahash/](https://github.com/zahash/)

## Contributing

1. Fork it (<https://github.com/zahash/dfcleaner/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
