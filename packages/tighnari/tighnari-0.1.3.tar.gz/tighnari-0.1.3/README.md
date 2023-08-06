# Tighnari

> This is part of `Pudgeland 💖 Open Source` ecosystems

An unofficial **[The Cat API](https://thecatapi.com)** wrapper for Python

## 📦 Packages

### 🐍 PyPI

```sh
pip install tighnari
```

## 🔎 Examples

```py
import tighnari

client = tighnari.Client()

for _ in range(5):
    print(client.images.search())
```
