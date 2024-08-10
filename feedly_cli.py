import requests
import argparse
import sys

class FeedlyService:
    BASE_URL = 'https://cloud.feedly.com'

    def search(self, query: str, count: int = 15, locale: str = None) -> dict:
        try:
            encoded_query = requests.utils.quote(query)
            url = f"{self.BASE_URL}/v3/search/feeds?query={encoded_query}&count={count}&locale={locale}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Error fetching search results: {e}")

    def get_feed_stream(self, feed_id: str, count: int = 15) -> dict:
        try:
            encoded_id = requests.utils.quote(feed_id)
            url = f"{self.BASE_URL}/v3/streams/contents?streamId={encoded_id}&count={count}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Error fetching feed stream: {e}")

    def get_entry(self, entry_id: str) -> dict:
        try:
            encoded_id = requests.utils.quote(entry_id)
            url = f"{self.BASE_URL}/v3/entries/{encoded_id}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Error fetching entry: {e}")

def main():
    parser = argparse.ArgumentParser(description="Feedly CLI Tool")
    subparsers = parser.add_subparsers(dest='command')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search for feeds')
    search_parser.add_argument('query', type=str, help='Search query')
    search_parser.add_argument('--count', type=int, default=15, help='Number of results to return')
    search_parser.add_argument('--locale', type=str, help='Locale for search results')

    # Get Feed Stream command
    stream_parser = subparsers.add_parser('stream', help='Get a feed stream')
    stream_parser.add_argument('feed_id', type=str, help='Feed ID')
    stream_parser.add_argument('--count', type=int, default=15, help='Number of entries to return')

    # Get Entry command
    entry_parser = subparsers.add_parser('entry', help='Get an entry')
    entry_parser.add_argument('entry_id', type=str, help='Entry ID')

    args = parser.parse_args()

    feedly_service = FeedlyService()

    try:
        if args.command == 'search':
            results = feedly_service.search(args.query, args.count, args.locale)
            print(results)
        elif args.command == 'stream':
            results = feedly_service.get_feed_stream(args.feed_id, args.count)
            print(results)
        elif args.command == 'entry':
            results = feedly_service.get_entry(args.entry_id)
            print(results)
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()


# search types:
    
#     python feedly_cli.py search {query} --count {count} --locale {lang/loc}
#         python feedly_cli.py search "python programming" --count 10 --locale en

#     python feedly_cli.py stream {feed_id} --count {article_count}
#         python feedly_cli.py stream feed_id --count 10

#     python feedly_cli.py entry {entry_id}


