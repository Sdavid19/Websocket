import json


# ---------------------------------------------------------
# 1. Python -> JSON FÁJLBA ÍRÁS
# ---------------------------------------------------------
def write_json_file():
    data = {
        "name": "Béla",
        "age": 25,
        "languages": ["Python", "JavaScript"],
        "admin": True,
        "users": [
            {"name": "Anna", "age": 20},
            {"name": "Bence", "age": 22}
        ]
    }

    with open("adatok.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("JSON fájl elkészült!")


# ---------------------------------------------------------
# 2. JSON FÁJLBÓL OLVASÁS -> Python objektum
# ---------------------------------------------------------
def read_json_file():
    with open("adatok.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Beolvasott adatok:", data)
    print("Első user neve:", data["users"][0]["name"])


# ---------------------------------------------------------
# 3. JSON FÁJL MÓDOSÍTÁSA (hozzáadás)
# ---------------------------------------------------------
def modify_json_file():
    # 1) beolvasás
    with open("adatok.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 2) módosítás
    data["users"].append({"name": "Csaba", "age": 30})

    # 3) visszaírás
    with open("adatok.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("JSON fájl módosítva!")


# ---------------------------------------------------------
# 4. Python -> JSON STRING
# ---------------------------------------------------------
def python_to_json_string():
    data = {"x": 10, "y": 20}
    json_str = json.dumps(data, indent=4)
    print("JSON string:")
    print(json_str)


# ---------------------------------------------------------
# 5. JSON STRING -> Python objektum
# ---------------------------------------------------------
def json_string_to_python():
    json_text = '{"x": 10, "y": 20, "z": 30}'
    data = json.loads(json_text)
    print("JSON stringből beolvasott érték:", data["z"])


# ---------------------------------------------------------
# FŐ PROGRAM – MINDENT FUTTAT
# ---------------------------------------------------------
if __name__ == "__main__":
    print("\n--- 1. Írás ---")
    write_json_file()

    print("\n--- 2. Olvasás ---")
    read_json_file()

    print("\n--- 3. Módosítás (hozzáadás) ---")
    modify_json_file()

    print("\n--- 4. Python -> JSON string ---")
    python_to_json_string()

    print("\n--- 5. JSON string -> Python ---")
    json_string_to_python()

    print("\nKÉSZ 🎉")
