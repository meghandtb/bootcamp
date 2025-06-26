🐼📰 ArticleManagerCLI

    Fetch, store, and summarize news articles — all from your terminal!

Welcome to ArticleManagerCLI – a cozy command-line app that helps you stay informed with the latest news, store your favorite reads, and get snappy summaries when you’re short on time. 🌍✨

Just give me a headline, and I’ll give you insight. 🧠

💡 Features

    🔎 Search & Fetch: Enter a query, fetch the latest headlines, and choose which article to save.

    📝 Auto Extract & Convert: Extract article content and store it as Markdown.

    💾 Save to Database: Save your selected articles to DynamoDB for later reading.

    📚 View Library: Browse all stored articles, including their titles and dates.

    🧠 Summarize: Use Ollama to get a TL;DR of any stored article — great for busy bees!

    🧹 Reset: Clear the database if you want a fresh start.


🗞️ _Get the news while they're hot!_ 🔥

---

## ⚙️ Setup

### 🧰 Prerequisites

- Python 3.8+
- Terraform
- AWS credentials configured (`aws configure`)
- `Ollama` installed and running locally

### 🪄 Setup using Makefile

| Command         | What it does                                         |
|----------------|------------------------------------------------------|
| `make install` | Installs all Python dependencies                     |
| `make clean`   | Removes Python cache files                           |
| `make run`     | Runs the CLI application (`cli.py`)                  |
| `make init`    | Initializes the Terraform backend                    |
| `make plan`    | Shows what Terraform will create                     |
| `make apply`   | Applies the Terraform configuration (DynamoDB, etc.) |
| `make destroy` | Destroys the Terraform infrastructure                |


