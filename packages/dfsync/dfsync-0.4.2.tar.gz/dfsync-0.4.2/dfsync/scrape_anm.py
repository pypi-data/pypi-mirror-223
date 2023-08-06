import json, hashlib, requests, os
from bs4 import BeautifulSoup
import concurrent.futures

METADATA_ATTRS = [
    "dencom",
    "dci",
    "formafarm",
    "conc",
    "codatc",
    "actter",
    "prescript",
    "ambalaj",
    "volumamb",
    "valabamb",
    "cim",
    "firmtarp",
    "firmtard",
    "nrdtamb",
]
LINK_ATTRS = [
    "linkrcp",
    "linkpro",
    "linkamb",
]
PDF_TARGET_DIR = {
    "linkrcp": "_RCP",
    "linkpro": "_PRO",
    "linkamb": "_AMB",
}


def make_identifier(metadata):
    nrdtamb = metadata.get("nrdtamb")
    codatc = metadata.get("codatc")
    cim = metadata.get("cim")
    if nrdtamb and codatc and cim:
        return hashlib.sha256(f"{nrdtamb}-{codatc}-{cim}".encode("utf8"), usedforsecurity=False).hexdigest()
    else:
        return None


def make_json_path(target_dir, identifier):
    json_dir = os.path.join(target_dir, identifier[:2])
    os.makedirs(json_dir, exist_ok=True)
    json_path = os.path.join(json_dir, f"{identifier}.json")
    return json_path


def scrape_pdf_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        records = []
        for link in soup.find_all("button"):
            metadata = {attr: link.get(f"data-{attr}") for attr in METADATA_ATTRS}
            identifier = make_identifier(metadata)
            metadata["identifier"] = identifier
            if not identifier:
                continue

            for attr in LINK_ATTRS:
                href = link.get(f"data-{attr}")
                if href and href.endswith(".pdf"):
                    metadata[attr] = href

            if metadata.get("linkpro"):
                records.append(metadata)
                save_record(identifier, metadata)
            else:
                print(f"Failed to get documents: {url} - {metadata['nrdtamb']}/{metadata['dencom']}")

        return records
    except Exception as e:
        print(f"Error scraping PDF links from {url}: {e}")
        return []


def save_record(identifier, metadata, target_dir="data-download"):
    for attr in LINK_ATTRS:
        url = metadata.get(attr)
        try:
            pdf_dir = os.path.join(target_dir, PDF_TARGET_DIR[attr])
            os.makedirs(pdf_dir, exist_ok=True)
            pdf_path = download_pdf(url, pdf_dir)
            metadata[f"{attr}-filepath"] = pdf_path
        except Exception as e:
            print(f"Error downloading {url}: {e}")

    json_path = make_json_path(target_dir, identifier)
    with open(json_path, "wb") as file:
        file.write(json.dumps(metadata).encode("utf8"))
    return json_path


def download_pdf(url, target_dir):
    filename = url.split("/")[-1]
    filepath = os.path.join(target_dir, filename)
    try:
        if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
            print(f"Already cached: {url}")
            return filepath
    except:
        # Re-download
        pass

    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(filepath, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"Downloaded: {url}")
    return filepath


def process_url(url):
    records = scrape_pdf_links(url)
    print(f"Processed: {len(records)} from {url}")


def generate_urls():
    urls = []
    base_url = "https://nomenclator.anm.ro/medicamente?page={}"
    pages = range(1562)
    for page_no in pages:
        urls.append(base_url.format(page_no + 1))

    return urls


def read_urls(filename="input.txt"):
    urls = []
    try:
        # Read the list of URLs from an input file
        with open("input.txt", "r") as file:
            urls = [line.strip() for line in file]
    except Exception as e:
        print(f"Failed to read URLs from {filename}: {e}")


def debug_scrape():
    urls = generate_urls()

    for url in urls[:2]:
        process_url(url)


def main_scrape():
    urls = generate_urls()

    # Use concurrent.futures.ProcessPoolExecutor to efficiently download and process the URLs
    with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
        executor.map(process_url, urls)


if __name__ == "__main__":
    main_scrape()
