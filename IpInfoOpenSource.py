import sys
import json
import urllib.request
import urllib.error

def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  Ошибка HTTP: {e.code}")
        return None
    except urllib.error.URLError:
        print("  Нет соединения с интернетом.")
        return None

def lookup(ip=""):
    url = f"https://ipapi.co/{ip}/json/" if ip else "https://ipapi.co/json/"
    data = fetch(url)
    if not data:
        return

    error = data.get("error") or data.get("reason")
    if error:
        print(f"  ❌  {error}")
        return

    fields = [
        ("IP",          data.get("ip",           "—")),
        ("Страна",      f"{data.get('country_name','—')} ({data.get('country','—')})"),
        ("Регион",      data.get("region",        "—")),
        ("Город",       data.get("city",          "—")),
        ("Почтовый",    data.get("postal",        "—")),
        ("Координаты",  f"{data.get('latitude','—')}, {data.get('longitude','—')}"),
        ("Часовой пояс",data.get("timezone",      "—")),
        ("Провайдер",   data.get("org",           "—")),
        ("ASN",         data.get("asn",           "—")),
    ]

    width = max(len(k) for k, _ in fields) + 2
    print()
    print("  ┌" + "─" * (width + 36) + "┐")
    for key, val in fields:
        label = f"  {key}".ljust(width + 2)
        print(f"  │ {label}  {val}")
    print("  └" + "─" * (width + 36) + "┘")
    print()

def main():
    print()
    print("  ╔══════════════════════════╗")
    print("  ║       IP INFO TOOL       ║")
    print("  ╚══════════════════════════╝")
    print("  Введи IP адрес или оставь пустым для своего IP.")
    print("  Напиши 'exit' чтобы выйти.")
    print()

    while True:
        try:
            raw = input("  > IP: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n  Выход.")
            break

        if raw.lower() in ("exit", "quit", "q"):
            print("  Выход.")
            break

        lookup(raw)

if __name__ == "__main__":
    main()