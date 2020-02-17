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
from dfcleaner import cleaner

df = cleaner.sanitize_column_names(df)
df = cleaner.preprocess(df, {'col0': float, 'col2': int}, 1.5, 'median')
```

## Development setup

```sh
pip3 install -r requirements.txt
```

Windows:

```sh
pip install -r requirements.txt
```

## Release History

- 0.2.1
  - fixed multiple underscore issue and add support for
    mulitple consecutive capital letters (DNSServer -> dns_server)
    in CamelCase to snake_case conversion
- 0.2.0
  - add default parameters to preprocess function
  - add parameter 'label_col' in preprocess() to remove
    rows where the label_col is null
  - sanitize_column_names() now converts CamelCase to snake_case
  - add parameter 'label_col' in remove_outliers() so that
    the label col will not be considered as a column to remove
    outliers from
  - suggest_conversion_dict() now suggests 'category' dtype to
    numeric columns that are actually categorical; like 'has_credit_card'
    that has 1 or 0 as values
  - add suggest_col_drop() to suggest which columns to drop (irrelevant columns)
    based on the column name; like ID, first_name, surname, ...
- 0.1.1
  - sanitize_column_names now keeps any already present underscores

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
