# CrypTax
**This project is still baking.**

CrypTax is a simple transaction gains reporting system for tax purposes. NOTE: this is an unofficial tool and should not be used for tax reporting purposes.

</br>

# Usage
Currently only the fills script works as there is an infinite loop issue with the account transactions resolution.  
To utilze the fills script:

0. Reference your CoinbasePro Fills report in the top of the `src/cryptax/fills.py` script:
```
...

txs_file = "path/to/your/fills_report.csv"
output_file = "path/to/exported_gains_report.csv"

...
```

1. Run the fills script using a python3 installation:
```
python3 ./fills.py
```

2. Your gains report will be dumped in the location of the output file you provided.
