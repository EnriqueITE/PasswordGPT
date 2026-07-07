![PasswordGPT Header Image](https://enriqueite.com/img/passwordGPTHeader.png "PasswordGPT Header Image")

# PasswordGPT

PasswordGPT is a small Python CLI that generates password dictionary candidates with the OpenAI API for authorized security audits.

Use it only on systems, accounts, or assessments where you have explicit permission.

## Installation

```bash
pip install -r requirements.txt
```

Set your OpenAI API key in an environment variable. Do not hard-code API keys in the source code.

PowerShell:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

Bash:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Optional: override the default model with `OPENAI_MODEL`.

```bash
export OPENAI_MODEL="gpt-5.5"
```

## Usage

```bash
python PasswordGPT.py -a [AMOUNT OF PASSWORDS] -w [WORDS SEPARATED BY COMMAS]
```

## Example

```bash
python PasswordGPT.py -a 5 -w finance,2023,investment,investors,money
```

The tool writes the generated candidates to `passwords.txt`, one candidate per line.

Example output:

```text
Finance2023
InvestmentMoney
Investors2023
MoneyInvestment
2023Finance
```

## Authorized Use Only

This software is provided for authorized auditing purposes only. Usage for any other purpose is prohibited. By accessing and using this software, you agree that you understand the limitations and risks associated with it and that you will comply with all applicable laws, regulations, and ethical guidelines.

The software is provided "as is" without warranty of any kind, express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, or non-infringement. The author disclaims responsibility for damages, liabilities, or losses arising from use or misuse of this software.

If you do not agree with these terms, do not use this software.
