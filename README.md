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
- Docker
- AWS credentials configured (`aws configure`)
- `Ollama` installed and running locally in a docker container

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

🚀 Usage

Launch the CLI:

make run

You’ll see a menu like this:

1. Fetch latest headlines and save an article
2. List all stored article titles and dates
3. Search articles by title and view content
4. Summarize an article using Ollama
5. Remove all entries from the database
6. Exit

Pick your option and enjoy the experience! 🎉
🧠 Powered by

    NewsData.io – Real-time news API

    Ollama – Lightweight, local language models

    Rich – Beautiful terminal outputs ✨

    Markdownify – HTML → Markdown

    AWS DynamoDB – Scalable cloud storage for your articles

🐣 Future Ideas

    Add tags or categories to articles

    Auto-fetch top news daily

    Export to Notion or Obsidian

    Summarize multiple articles into one digest

🤝 Contributing

Pull requests are welcome! Help us improve by fixing bugs, adding features, or making it even cuter. 🐹
🐾 Final Words

Stay curious. Stay informed. And remember:

    The best stories are the ones you understand.

Happy reading! 💌
