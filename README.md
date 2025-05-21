# AWS-Lambda-boto3-automation
Automate AWS cloud operations using AWS Lambda functions powered by Boto3. This repository contains Python scripts for event-driven automation of AWS services like EC2, S3, IAM, and more, enabling scalable and efficient cloud management.

# Installing boto3 in PyCharm (Step-by-Step Guide)

This guide will help you install the `boto3` library in your PyCharm project.

## Step 1: Open PyCharm

Launch PyCharm and open your project or create a new one.

## Step 2: Open the Python Interpreter Settings

1. Go to the top menu and click on `File`.
2. Select `Settings` (or `Preferences` on macOS).
3. In the left pane, navigate to `Project: <your_project_name>` > `Python Interpreter`.

## Step 3: Install boto3

1. Click on the **`+`** icon (Add Package) on the right side of the Python Interpreter window.
2. In the search bar, type `boto3`.
3. Select `boto3` from the list.
4. Click on the `Install Package` button at the bottom.

PyCharm will install the `boto3` library and its dependencies.

## Step 4: Verify Installation

To confirm that boto3 is installed:

1. Open a Python file in your project.
2. Add the following import statement:

```python
import boto3
```

3. Run the file or use the Python console to ensure no errors appear.

## Alternative Method: Use Terminal in PyCharm

You can also install boto3 using the terminal built into PyCharm:

1. Click on the `Terminal` tab at the bottom of PyCharm.
2. Run the following command:

```bash
pip install boto3
```

---

Now you're ready to use `boto3` in your PyCharm project!
