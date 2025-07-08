import json
import requests
import boto3
from readabilipy import simple_json_from_html_string
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
TABLE_NAME = "articles"

def fetch_headlines(query="", language="en", apikey=""):
    url = f"https://newsdata.io/api/1/latest?apikey={apikey}&q={query}&language={language}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("results", [])

def extract_article_json(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        article_json = simple_json_from_html_string(response.text, use_readability=True)
        return article_json

    except requests.exceptions.RequestException as e:
        print(f"[Error] Failed to fetch the page: {e}")
        return None
    except Exception as e:
        print(f"[Error] Failed to parse article content: {e}")
        return None

def load_article_to_dynamodb(title, date, content, table_name=TABLE_NAME):
    try:
        table = dynamodb.Table(table_name)
        table.put_item(Item={
            "title": title,
            "date": date,
            "content": content
        })
        print(f"Article stored: {title} ({date})")
    except Exception as e:
        print(f"[Error] Failed to store item in DynamoDB: {e}")

def get_article_by_title_date(title, table_name=TABLE_NAME):
    table = dynamodb.Table(table_name)
    try:
        response = table.get_item(
            Key={
                "title": title
            }
        )
        return response.get("Item")
    except Exception as e:
        print(f"[Error] Failed to retrieve item: {e}")
        return None

def get_all_articles(table_name=TABLE_NAME):
    table = dynamodb.Table(table_name)
    try:
        response = table.scan()
        return response.get("Items", [])
    except Exception as e:
        print(f"[Error] Scan failed: {e}")
        return []

def print_all_article_titles_and_dates(table_name=TABLE_NAME):
    articles_from_dynamo = get_all_articles(table_name)
    print(f"Fetched {len(articles_from_dynamo)} articles.\n")
    for article in articles_from_dynamo:
        title = article.get("title", "<no title>")
        date = article.get("date", "<no date>")
        print(f"Title: {title} | Date: {date}")

def get_article_content_by_title(title, table_name=TABLE_NAME):
    table = dynamodb.Table(table_name)
    try:
        response = table.query(
            KeyConditionExpression=Key("title").eq(title)
        )
        items = response.get("Items", [])
        return [{"date": item["date"], "content": item.get("content", "")} for item in items]
    except Exception as e:
        print(f"[Error] Failed to query articles by title: {e}")
        return []

def query_ollama(model: str, prompt: str, stream=False) -> str:
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream,
    }
    try:
        if not stream:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        else:
            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line.decode("utf-8"))
                        text = data.get("response", "")
                        yield text
    except requests.RequestException as e:
        if stream:
            yield f"[Error] Request exception: {e}"
        else:
            return f"[Error] Request exception: {e}"

def truncate_dynamodb_table(console, table_name=TABLE_NAME):
    table = dynamodb.Table(table_name)

    try:
        key_schema = table.key_schema
        key_names = [key["AttributeName"] for key in key_schema]

        deleted_count = 0
        scan_kwargs = {}

        while True:
            response = table.scan(**scan_kwargs)
            items = response.get("Items", [])
            if not items:
                break

            with table.batch_writer() as batch:
                for item in items:
                    key = {k: item[k] for k in key_names}
                    batch.delete_item(Key=key)
                    deleted_count += 1

            if "LastEvaluatedKey" in response:
                scan_kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
            else:
                break

        if deleted_count == 0:
            console.print("[yellow]\n⚠️  The database is already empty. No items to delete.[/yellow]")
        else:
            console.print(f"[green]✅ Successfully deleted {deleted_count} item(s) from '{table_name}'.[/green]")

    except Exception as e:
        console.print(f"[red][Error] Failed to truncate table: {e}[/red]")
