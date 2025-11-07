# 🚀 Lambda Deployment Automation (Python + Boto3)

![Build Status](https://github.com/Gwerdonatus/lambda-deploy-demo/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A lightweight **AWS Lambda deployment automation tool** built with Python and Boto3.
It helps developers quickly **create or update** Lambda functions directly from a `.zip` package — perfect for small teams, personal projects, or CI/CD pipelines.

---

## ✨ Features

* 📦 Deploys or updates AWS Lambda functions automatically.
* ⚙️ Supports custom runtime, memory size, and timeout settings.
* 🔒 Reads config from **environment variables** (safer than plain JSON).
* 🪶 Minimal setup — just Python, Boto3, and your AWS credentials.
* 🧱 Clean, reusable structure you can plug into your own automation pipelines.
* 🧪 Includes **dry-run mode** and **unit tests** (mocked Boto3).
* 🧰 Includes **ZIP build script** for packaging your Lambda automatically.

---

## 🧠 How It Works

The script:

1. Reads your packaged Lambda code (`lambda.zip`) or builds it from source.
2. Loads configuration from environment variables or `config.json`.
3. Connects to AWS Lambda via Boto3.
4. Checks if the function exists:

   * If yes → updates the code.
   * If no → creates a new function.
5. Returns the function ARN or an error message.

---

## ⚡ Getting Started

### 🔧 Prerequisites

* Python 3.9+
* AWS CLI configured with credentials (`aws configure`)
* Boto3 installed

```bash
pip install boto3
```

---

### 🪜 Setup Steps

```bash
# 1. Clone the repo
git clone https://github.com/Gwerdonatus/lambda-deploy-demo.git
cd lambda-deploy-demo

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate  # (Windows)
# or
source venv/bin/activate  # (Mac/Linux)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Build ZIP package (optional)
python build_zip.py

# 5. Test in dry-run mode
python deploy_lambda.py --dry-run
```

---

## 🧩 Configuration

You can configure via **environment variables** (recommended):

```bash
export FUNCTION_NAME=my-test-function
export ROLE_ARN=arn:aws:iam::123456789012:role/lambda-role
export HANDLER=lambda_function.lambda_handler
export RUNTIME=python3.9
export TIMEOUT=30
export MEMORY_SIZE=128
export ZIP_FILE=lambda.zip
```

Or use a fallback `config.json`:

```json
{
  "function_name": "my-test-function",
  "zip_file_path": "lambda.zip",
  "role_arn": "arn:aws:iam::123456789012:role/lambda-role",
  "handler": "lambda_function.lambda_handler",
  "runtime": "python3.9",
  "timeout": 30,
  "memory_size": 128
}
```

---

## 📦 Example Lambda Function (`lambda_function.py`)

```python
def lambda_handler(event, context):
    message = "Hello from Lambda Deployment Automation!"
    print(message)
    return {
        "statusCode": 200,
        "body": message
    }
```

---

## 🧰 Example Build Script (`build_zip.py`)

```python
import zipfile
import os

def build_zip(zip_name="lambda.zip", source_files=None):
    if source_files is None:
        source_files = ["lambda_function.py"]

    with zipfile.ZipFile(zip_name, "w") as zf:
        for file in source_files:
            if os.path.exists(file):
                zf.write(file)
                print(f"✅ Added {file}")
            else:
                print(f"⚠️ File not found: {file}")

    print(f"🎯 Build complete: {zip_name}")

if __name__ == "__main__":
    build_zip()
```

---

## 📸 Example Output

```bash
(venv) PS C:\lambda-demo> python deploy_lambda.py --dry-run
🔧 Dry run active — no deployment to AWS
✅ Lambda "my-test-function" ready to deploy
🚀 Demo completed successfully
```

*(Add a real screenshot here if you can — it boosts visual appeal!)*

---

## 🧪 Running Unit Tests

This project includes a simple test suite using **unittest** and **moto** (to mock AWS Lambda).

```bash
pip install moto pytest
pytest
```

The CI workflow (`.github/workflows/ci.yml`) automatically runs tests and dry-run builds before publishing.

---

## 🔐 Security Notes

* Never commit your AWS credentials to GitHub.
* Use **IAM roles** with least privilege access.
* In CI/CD pipelines, use **encrypted secrets** for AWS keys.
* Prefer **environment variables** for sensitive config values.

---

## 🏷️ Release

Version **v1.0** marks the first stable release of the Lambda Deployment Automation script —
including ZIP build support, environment variable configuration, and CI test integration.

To create a tagged release manually:

```bash
git tag -a v1.0 -m "Initial stable release"
git push origin v1.0
```

---

## 🤝 Contributing

Pull requests and issues are welcome!
If you’d like to improve or extend the script (e.g., add multi-function deployment, better logs, or more tests), open a PR.

---

## 🪪 License

This project is licensed under the [MIT License](LICENSE).

---

### 🧭 Author

**Gwer Donatus**
💻 Python & Django Developer
🌐 [GitHub](https://github.com/Gwerdonatus) | 📧 [donatusgwer@gmail.com](mailto:donatusgwer@gmail.com) | 💬 WhatsApp: +234 811 627 6112

> “Automation simplifies life — this script is a small step toward smarter deployment.”
