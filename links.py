import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from rich import print

print('''[red]\t     _        _/ _
\t|/|//_|/_//_///_\ 
\t       _/         
\t [red][[white]coded by [cyan]ryuku[red]] 🥷
''')

def main():
    parser = argparse.ArgumentParser(description='extracts links from a web page.')
    parser.add_argument('-u', '--url', required=True, help='target URL to extract links from')
    parser.add_argument('-o', '--output', help='Save links into a file')
    args = parser.parse_args()

    url = args.url

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(e)
        exit(1)

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(e)
        exit(1)

    domain = urlparse(url).scheme + '://' + urlparse(url).hostname

    links = set()
    for tag in soup.find_all(True):
        for attribute in tag.attrs:
            if attribute.startswith('href') or attribute.startswith('src'):
                value = tag.get(attribute)
                if value:
                    if not value.startswith('http'):
                        value = urljoin(domain, value)
                    links.add(value)

    if not links:
        print(f'[red][✖] [white]No links found at [red]{url} 💀')
        exit(0)

    unique_links = list(links)
    unique_links.sort()

    if args.output:
        try:
            with open(args.output, 'w') as f:
                for link in unique_links:
                    f.write(link + '\n')
            print(f'[green][✓] [white]Saved [green]{len(unique_links)}[white] links 🔗 to [cyan]{args.output}[white].')
        except Exception as e:
            pass
    else:
        for i, link in enumerate(unique_links):
            print(f'[green]{i+1}. [white]{link}')

if __name__ == '__main__':
    main()
