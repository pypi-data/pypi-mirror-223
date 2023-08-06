import os, shutil


def make_json_path(target_dir, identifier):
    json_dir = os.path.join(target_dir, identifier[:2])
    os.makedirs(json_dir, exist_ok=True)
    json_path = os.path.join(json_dir, f"{identifier}.json")
    return json_path


def main_reorg(target_dir="data-download"):
    count = 0
    for entry in os.scandir(target_dir):
        file_name = entry.name.lower()
        if entry.name.endswith(".json"):
            identifier, ext = file_name.split(".")
            destination = make_json_path(target_dir, identifier)
            shutil.move(entry.path, destination)
            count += 1
    print(f"JSON files: {count}")


def main_scan(target_dir="data-download"):
    size = 0
    for entry in os.scandir(target_dir):
        if os.path.isdir(entry.path):
            size += main_scan(entry.path)
        elif os.path.isfile(entry.path):
            size += os.path.getsize(entry.path)
    return size


if __name__ == "__main__":
    print(main_scan())
