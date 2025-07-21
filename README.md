# receipt-statement-linker

Python program that links receipts/invoices to bank statements, extracting data from both into a single json file.

# Comamnd Line Options
- `--receipt-input receipt.jpg` - Receipt/invoice files to process
- `--statement-input statement.pdf` - Bank statement files to process
- `--receipt-output output.json` - JSON filepath for output
- `--categorize` - Turn categorization on
- `--categories category1 category2 ...` - Categories to use for categorization (optional)

# Categorization
With categorization on, each entry will include a category for the transaction, and categorization for each item within the associated receipt. The default categories are:

```py
DEFAULT_CATEGORIES = [
  "GROCERIES",
  "EATING_OUT",
  "TRANSPORTATION",
  "HOUSING",
  "HEALTHCARE",
  "PERSONAL_CARE",
  "ENTERTAINMENT",
  "SAVINGS_AND_INVESTMENTS",
  "DEBT_PAYMENT",
  "UTILITIES",
  "MISC",
]
```

Custom categories can be specified using `--categories category1 category2 ...`.

Only labels may not be enough context for the categorization. To add more context to give to the model, you can add context under `$XDG_DATA_HOME/receipt_statement_linker/user_instructions`.

# Example

A sample invoice and statement can be found under `example/`. The output of running it on these sample docs using the args `--receipt-input example/invoice-sample.pdf --statement-input example/bank-statement-sample.pdf --categorize --receipt-output example/example.json` is found under `example/example.json`
