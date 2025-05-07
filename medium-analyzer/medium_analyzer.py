from pinecone import Pinecone

from config.settings import get_settings

settings = get_settings()

pc = Pinecone(api_key=settings.PINECONE_API_KEY)


def main():
    print("Hello from medium-analyzer!")


if __name__ == "__main__":
    main()
