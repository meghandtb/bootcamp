import requests
import os
from dotenv import load_dotenv
from helpers import fetch_headlines, extract_article_json, query_ollama, load_article_to_dynamodb, print_all_article_titles_and_dates, get_article_content_by_title, get_all_articles, truncate_dynamodb_table
from markdownify import markdownify as md
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.spinner import Spinner
from rich.live import Live
from rich.text import Text
from rich.console import Group
from time import sleep

load_dotenv()
console = Console()

ascii_banner = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⢀⣴⠟⠉⠀⠀⠀⠈⠻⣦⡀⠀⠀⠀⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣀⢀⣾⠿⠻⢶⣄⠀⠀⣠⣶⡿⠶⣄⣠⣾⣿⠗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⢻⣿⣿⡿⣿⠿⣿⡿⢼⣿⣿⡿⣿⣎⡟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟⠉⠛⢛⣛⡉⠀⠀⠙⠛⠻⠛⠑⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣧⣤⣴⠿⠿⣷⣤⡤⠴⠖⠳⣄⣀⣹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣀⣟⠻⢦⣀⡀⠀⠀⠀⠀⣀⡈⠻⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⡿⠉⡇⠀⠀⠛⠛⠛⠋⠉⠉⠀⠀⠀⠹⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⡟⠀⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠈⠑⠪⠷⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣦⣼⠛⢦⣤⣄⡀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠑⠢⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⠲⠖⠛⠻⣿⡿⠛⠉⠉⠻⠷⣦⣽⠿⠿⠒⠚⠋⠉⠁⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢦⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⠛⠁⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢣⠀⠀⠀
⠀⠀⠀⠀⣰⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣑⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡇⠀⠀
⠀⠀⠀⣰⣿⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣧⣄⠀⠀⠀⠀⠀⠀⢳⡀⠀
⠀⠀⠀⣿⡾⢿⣀⢀⣀⣦⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⣫⣿⡿⠟⠻⠶⠀⠀⠀⠀⠀⢳⠀
⠀⠀⢀⣿⣧⡾⣿⣿⣿⣿⣿⡷⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⢀⡴⢿⣿⣧⠀⡀⠀⢀⣀⣀⢒⣤⣶⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇
⠀⠀⡾⠁⠙⣿⡈⠉⠙⣿⣿⣷⣬⡛⢿⣶⣶⣴⣶⣶⣶⣤⣤⠤⠾⣿⣿⣿⡿⠿⣿⠿⢿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇
⠀⣸⠃⠀⠀⢸⠃⠀⠀⢸⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⠟⡉⠀⠀⠀⠈⠙⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇
⠀⣿⠀⠀⢀⡏⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⠿⠿⠛⠛⠉⠁⠀⠀⠀⠀⠀⠉⠠⠿⠟⠻⠟⠋⠉⢿⣿⣦⡀⢰⡀⠀⠀⠀⠀⠀⠀⠁
⢀⣿⡆⢀⡾⠀⠀⠀⠀⣾⠏⢿⣿⣿⣿⣯⣙⢷⡄⠀⠀⠀⠀⠀⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣿⣻⢿⣷⣀⣷⣄⠀⠀⠀⠀⢸⠀
⢸⠃⠠⣼⠃⠀⠀⣠⣾⡟⠀⠈⢿⣿⡿⠿⣿⣿⡿⠿⠿⠿⠷⣄⠈⠿⠛⠻⠶⢶⣄⣀⣀⡠⠈⢛⡿⠃⠈⢿⣿⣿⡿⠀⠀⠀⠀⠀⡀
⠟⠀⠀⢻⣶⣶⣾⣿⡟⠁⠀⠀⢸⣿⢅⠀⠈⣿⡇⠀⠀⠀⠀⠀⣷⠂⠀⠀⠀⠀⠐⠋⠉⠉⠀⢸⠁⠀⠀⠀⢻⣿⠛⠀⠀⠀⠀⢀⠇
⠀⠀⠀⠀⠹⣿⣿⠋⠀⠀⠀⠀⢸⣧⠀⠰⡀⢸⣷⣤⣤⡄⠀⠀⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡆⠀⠀⠀⠀⡾⠀⠀⠀⠀⠀⠀⢼⡇
⠀⠀⠀⠀⠀⠙⢻⠄⠀⠀⠀⠀⣿⠉⠀⠀⠈⠓⢯⡉⠉⠉⢱⣶⠏⠙⠛⠚⠁⠀⠀⠀⠀⠀⣼⠇⠀⠀⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀⡇
⠀⠀⠀⠀⠀⠀⠻⠄⠀⠀⠀⢀⣿⠀⢠⡄⠀⠀⠀⣁⠁⡀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⢀⣐⡟⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⢠⡇
"""

ascii_text = r"""
,---.   .--.    .-''-.  .--.      .--.   .-'''-.          ________   .---.        ____       .-'''-. .---.  .---.  
|    \  |  |  .'_ _   \ |  |_     |  |  / _     \        |        |  | ,_|      .'  __ `.   / _     \|   |  |_ _|  
|  ,  \ |  | / ( ` )   '| _( )_   |  | (`' )/`--'        |   .----',-./  )     /   '  \  \ (`' )/`--'|   |  ( ' )  
|  |\_ \|  |. (_ o _)  ||(_ o _)  |  |(_ o _).           |  _|____ \  '_ '`)   |___|  /  |(_ o _).   |   '-(_{;}_) 
|  _( )_\  ||  (_,_)___|| (_,_) \ |  | (_,_). '.         |_( )_   | > (_)  )      _.-`   | (_,_). '. |      (_,_)  
| (_ o _)  |'  \   .---.|  |/    \|  |.---.  \  :        (_ o._)__|(  .  .-'   .'   _    |.---.  \  :| _ _--.   |  
|  (_,_)\  | \  `-'    /|  '  /\  `  |\    `-'  |        |(_,_)     `-'`-'|___ |  _( )_  |\    `-'  ||( ' ) |   |  
|  |    |  |  \       / |    /  \    | \       /         |   |       |        \\ (_ o _) / \       / (_{;}_)|   |  
'--'    '--'   `'-..-'  `---'    `---`  `-...-'          '---'       `--------` '.(_,_).'   `-...-'  '(_,_) '---'  
                                                                                                                   
"""

NEWSDATA_API_KEY = os.getenv('NEWSDATA_API_KEY')

headlines = fetch_headlines("climate", "en", NEWSDATA_API_KEY)

def banner():
    console.clear()
    console.print(ascii_banner, style="bold blue")
    console.print(ascii_text, style="bold cyan")
    console.print("[bold red]Welcome! Get the news while they're hot![/bold red] 🔥")

def fetch_and_store_article():
    query = Prompt.ask("Enter search query for headlines")
    headlines = fetch_headlines(query=query, apikey=NEWSDATA_API_KEY)
    if not headlines:
        console.print("[red]No headlines found.[/red]")
        return

    # Show top 5 headlines for user to pick
    table = Table(title="Select an article to save")
    table.add_column("Index", style="cyan", no_wrap=True)
    table.add_column("Title", style="green")
    table.add_column("Date", style="magenta")

    for i, headline in enumerate(headlines[:5], start=1):
        table.add_row(str(i), headline.get("title", "N/A"), headline.get("pubDate", "N/A"))
    console.print(table)

    choice = IntPrompt.ask("Choose article index to save", choices=[str(i) for i in range(1, min(len(headlines),5)+1)])
    selected = headlines[choice - 1]

    article_url = selected.get("link")
    article_title = selected.get("title")
    article_date = selected.get("pubDate")

    article_json = extract_article_json(article_url)
    if not article_json or 'content' not in article_json:
        console.print("[red]Failed to extract article content.[/red]")
        return

    content = article_json['content']
    article_md_content = md(content)
    
    # console.clear()

    load_article_to_dynamodb(article_title, article_date, article_md_content)
    console.print(f"\n[green]Article '{article_title}' saved successfully![/green]")

def list_articles():
    articles = get_all_articles()
    if not articles:
        console.print("[yellow]No articles stored yet. Choose option 1 so you can add some. [/yellow]")
        return

    table = Table(title="articles")
    table.add_column("Title", style="cyan")
    table.add_column("Date", style="magenta")

    for art in articles:
        table.add_row(art.get("title", "N/A"), art.get("date", "N/A"))
    console.print(table)

def view_article_content():
    articles = get_all_articles()
    if not articles:
        console.print("[bold yellow]⚠️  No articles are currently stored in the database.[/bold yellow]")
        return

    titles = [article["title"] for article in articles]

    # Show titles in a rich table
    table = Table(title="📰 Available Articles")
    table.add_column("Index", justify="right")
    table.add_column("Title", style="cyan", overflow="fold")

    for idx, title in enumerate(titles, start=1):
        table.add_row(str(idx), title)

    console.print(table)

    try:
        choice = IntPrompt.ask(
            "Enter the index of the article to view",
            choices=[str(i) for i in range(1, len(titles) + 1)]
        )
        selected_title = titles[choice - 1]
    except (ValueError, IndexError):
        console.print("[red]Invalid selection.[/red]")
        return

    selected_articles = get_article_content_by_title(selected_title)
    if not selected_articles:
        console.print(f"[yellow]No content found for '{selected_title}'.[/yellow]")
        return

    for article in selected_articles:
        console.rule(f"🗓️  Date: {article['date']}")
        console.print(article['content'])

def summarize_article():
    prompt = """
        Summarize the following text in one clear and concise paragraph, 
        capturing the key ideas without missing critical points. 
        Ensure the summary is easy to understand and avoids excessive detail.
        Avoid technical jargon and prioritize simplicity.
        Avoid answering other rhetorical questions.
    """

    articles = get_all_articles()
    if not articles:
        console.print("[yellow]No articles found in the database. Choose option 1 so you can add some. [/yellow]")
        return

    titles = [article["title"] for article in articles]

    # Show titles in a rich table
    table = Table(title="📰 Available Articles")
    table.add_column("Index", justify="right")
    table.add_column("Title", style="cyan", overflow="fold")

    for idx, title in enumerate(titles, start=1):
        table.add_row(str(idx), title)

    console.print(table)

    choice = Prompt.ask("\nEnter the number of the article to summarize", choices=[str(i) for i in range(1, len(titles) + 1)])
    selected_title = titles[int(choice) - 1]

    articles_to_summarize = get_article_content_by_title(selected_title)
    if not articles_to_summarize:
        console.print(f"[yellow]No articles found with title '{selected_title}'.[/yellow]")
        return

    for article in articles_to_summarize:
        # spinner = Spinner("bouncingBar", text="🐼 Panda is thinking... please wait!")
        # with Live(spinner, console=console, refresh_per_second=12):
        #     summary = query_ollama("phi4-mini:3.8b", f"Summarize the following article in a few sentences: {article['content']}", stream=False)
        # console.rule(f"Summary for article dated {article['date']}")
        # console.print(summary)

        spinner = Spinner("bouncingBar", text="🦙 Lama is thinking... Please wait!")
        summary_text = Text()
        with Live(Group(spinner, summary_text), console=console, refresh_per_second=12) as live:
            for chunk in query_ollama("phi4-mini:3.8b", f"{prompt} Title: {selected_title} Content: {article['content']}", stream=True):
                summary_text.append(chunk)
                live.update(Group(spinner, summary_text))

        console.print()
        console.rule("[ [bold red]Summary completed![/bold red] ]")

def main_menu():
    console.print()
    console.rule("[ [bold cyan]Article Manager CLI[/bold cyan] ]")
    console.print()
    console.print("1. Fetch latest headlines and save an article")
    console.print("2. List all stored article titles and dates")
    console.print("3. Search articles by title and view content")
    console.print("4. Summarize an article using Ollama")
    console.print("5. Remove all entries from the database")
    console.print("6. Exit")
    console.print()

def main():
    banner()
    while True:
        main_menu()
        choice = IntPrompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6"])
        if choice == 1:
            fetch_and_store_article()
        elif choice == 2:
            list_articles()
        elif choice == 3:
            view_article_content()
        elif choice == 4:
            summarize_article()
        elif choice == 5:
            truncate_dynamodb_table()
        elif choice == 6:
            console.print("[bold green]Goodbye![/bold green]")
            break

if __name__ == "__main__":
    main()

