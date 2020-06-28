from urllib.parse import urlparse


def domain_name(url):
    parsed = urlparse(url if "//" in url else f"//{url}")
    hostname = parsed.hostname
    parts = hostname.split('.')
    return parts[1] if parts[0] == 'www' else parts[0]


if __name__ == '__main__':
    assert domain_name("http://google.com") == "google"
    assert domain_name("http://google.co.jp") == "google"
    assert domain_name("www.xakep.ru") == "xakep"
    assert domain_name("https://youtube.com") == "youtube"
