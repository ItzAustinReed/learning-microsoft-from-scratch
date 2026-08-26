import re
import urllib.request
from pathlib import Path


MICROSOFT_DOMAINS = (
    "learn.microsoft.com",
    "azure.microsoft.com",
    "microsoft.com",
)


def extract_urls(text: str) -> list[str]:
    return re.findall(r"https?://[^\s)>\"]+", text)


def check_url(url: str) -> bool:
    try:
        request = urllib.request.Request(
            url,
            method="HEAD",
            headers={"User-Agent": "Mozilla/5.0"},
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            return 200 <= response.status < 400

    except Exception:
        return False


def main() -> None:
    markdown_files = list(Path(".").rglob("*.md"))

    urls = set()

    for file in markdown_files:
        text = file.read_text(encoding="utf-8")

        for url in extract_urls(text):
            if any(domain in url for domain in MICROSOFT_DOMAINS):
                urls.add(url)

    for url in sorted(urls):
        status = "OK" if check_url(url) else "FAILED"
        print(f"[{status}] {url}")


if __name__ == "__main__":
    main()
