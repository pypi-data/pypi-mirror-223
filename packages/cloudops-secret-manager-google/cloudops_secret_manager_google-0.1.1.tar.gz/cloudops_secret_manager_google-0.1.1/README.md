# cloudops-secret-manager-google

Easily manage your JSON secrets in Google Secret Manager.

## Installation

```bash
pip install cloudops-secret-manager-google
```

## Usage

```python

from cloudops.secret_manager.google import Secret

secret = Secret("your-project-id", "your-secret")

# Create your secret
secret.create()

# Push a new version of your secret
data = {
    "key": "value"
}
secret.push(data)

# Pull dict
secret_data = secret.pull()

```
