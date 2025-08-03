# receipt-statement-linker

Python program that links receipts/invoices to bank statements, extracting data from both into a single json file.

Sample receipt:

<img width="856" height="738" alt="image" src="https://github.com/user-attachments/assets/a9e1d095-44b4-44f1-9b6b-fe4bd6897e6f" />

Sample bank statement transaction:

<img width="639" height="65" alt="image" src="https://github.com/user-attachments/assets/5542d8ac-cc42-42ff-b523-b39f36569579" />

Sample linker output:

<img width="1257" height="601" alt="image" src="https://github.com/user-attachments/assets/e7e73bf0-049b-49d4-ac68-2288b3c6f94a" />





# Command Line Options
- `--receipt-input receipt.jpg` - Receipt/invoice files to process
- `--statement-input statement.pdf` - Bank statement files to process
- `--receipt-output output.json` - JSON filepath for output
- `--categorize` - Turn categorization on
- `--categories category1 category2 ...` - Categories to use for categorization (optional)

# Config file
The config file can be found at `$XDG_CONFIG_HOME/receipt_statement_linker/config.toml`. The config file has the following fields:
- `transcription_model` - model used for receipt & statement transcription.
- `categorization_model` - model used for receipt & statement categorization, if enabled.
- `matching_model` - model used for matching receipts to statement transactions when multiple transaction prices match the receipt price.
- `categorization_notes` - notes to provide extra context to the model when categorizing

Models are litellm model strings. You can find them by going [here](https://docs.litellm.ai/docs/providers) and selecting a provider.

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

Only labels may not be enough context for the categorization. To add more context to give to the model, you can add context in the config file like so:
```toml
categorization_notes = "'Liberty' is a theatre, so it falls under entertainment."
```

# Supported Filetypes
The filetypes that are supported are based on whatever model is selected. The defualt is Gemini 2.5 Flash, and supported filetypes for this model can be found [here](https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-flash).

# Example
A sample invoice and statement can be found under `example/`. The output of running the following command can be found at `example/example.json`:
```bash
uvx receipt-statement-linker \
          --receipt-input     example/invoice-sample.pdf \
          --statement-input   example/bank-statement-sample.pdf \
          --categorize \
          --receipt-output    example/example.json
```
