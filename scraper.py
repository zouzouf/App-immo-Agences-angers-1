import json
import re
import requests
from bs4 import BeautifulSoup

# En-tête pour simuler un vrai navigateur et éviter certains blocages simples
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"
}

MAX_PRICE = 125000

def clean_price(price_str):
    """Extrait la valeur numérique d'un prix sous forme de texte."""
    if not price_str:
        return 0
    cleaned = re.sub(r"[^\d]", "", price_str)
    return int(cleaned) if cleaned else 0

# --- MODULES DE SCRAPING PAR AGENCE ---

def scrape_blot():
    """Scrape les annonces d'achat d'appartements sur Angers via Blot Immobilier."""
    annonces = []
    # URL de recherche d'appartements à acheter sur Angers à moins de 125 000 €
    url = "https://www.blot-immobilier.fr/achat/appartement/angers/?prix_max=125000"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return annonces

        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.select("article.card-bien, div.annonces-item")

        for card in cards:
            title_elem = card.select_one(".card-bien__title, .title")
            price_elem = card.select_one(".card-bien__price, .price")
            link_elem = card.select_one("a[href]")
            desc_elem = card.select_one(".card-bien__desc, .description")

            if title_elem and price_elem and link_elem:
                price = clean_price(price_elem.text)
                link = link_elem["href"]
                if not link.startswith("http"):
                    link = "https://www.blot-immobilier.fr" + link

                annonces.append({
                    "title": title_elem.text.strip(),
                    "price": price,
                    "agency": "Blot Immobilier",
                    "description": desc_elem.text.strip() if desc_elem else "Appartement à vendre sur Angers.",
                    "url": link
                })
    except Exception as e:
        print(f"Erreur lors du scraping de Blot Immobilier : {e}")
    return annonces

def scrape_nicole_joubert():
    """Scrape les annonces sur Nicole Joubert (Agence locale d'Angers)."""
    annonces = []
    url = "https://www.nicolejoubert.fr/achat/angers/appartement"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return annonces

        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.select(".annonce-item, .property-item")

        for card in cards:
            title_elem = card.select_one(".title, h2, h3")
            price_elem = card.select_one(".price, .prix")
            link_elem = card.select_one("a[href]")
            desc_elem = card.select_one(".description, .text")

            if price_elem and link_elem:
                price = clean_price(price_elem.text)
                if price <= MAX_PRICE and price > 0:
                    link = link_elem["href"]
                    if not link.startswith("http"):
                        link = "https://www.nicolejoubert.fr" + link

                    annonces.append({
                        "title": title_elem.text.strip() if title_elem else "Appartement Angers",
                        "price": price,
                        "agency": "Nicole Joubert",
                        "description": desc_elem.text.strip() if desc_elem else "Description disponible sur le site de l'agence.",
                        "url": link
                    })
    except Exception as e:
        print(f"Erreur lors du scraping de Nicole Joubert : {e}")
    return annonces

def scrape_square_habitat():
    """Scrape les annonces sur Square Habitat Crédit Agricole (Angers)."""
    annonces = []
    url = "https://www.squarehabitat.fr/ventes/appartement/angers?prix_max=125000"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return annonces

        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.select(".card-property, .bien-item")

        for card in cards:
            title_elem = card.select_one(".property-title, .title")
            price_elem = card.select_one(".property-price, .prix")
            link_elem = card.select_one("a[href]")

            if price_elem and link_elem:
                price = clean_price(price_elem.text)
                if price <= MAX_PRICE and price > 0:
                    link = link_elem["href"]
                    if not link.startswith("http"):
                        link = "https://www.squarehabitat.fr" + link

                    annonces.append({
                        "title": title_elem.text.strip() if title_elem else "Appartement Angers",
                        "price": price,
                        "agency": "Square Habitat",
                        "description": "Consultez l'annonce sur le site de l'agence pour plus de détails.",
                        "url": link
                    })
    except Exception as e:
        print(f"Erreur lors du scraping de Square Habitat : {e}")
    return annonces

# --- SCRIPT PRINCIPAL ---

def main():
    print("Début du scraping des agences d'Angers...")
    all_annonces = []

    # Exécution des scrapers
    all_annonces.extend(scrape_blot())
    all_annonces.extend(scrape_nicole_joubert())
    all_annonces.extend(scrape_square_habitat())

    # Filtrage strict final sur le prix < 125 000 €
    filtered_annonces = [item for item in all_annonces if 0 < item["price"] < MAX_PRICE]

    # Déduplication par URL
    unique_annonces = {item["url"]: item for item in filtered_annonces}.values()
    result = list(unique_annonces)

    # Sauvegarde au format JSON pour l'application Web
    with open("annonces.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Scraping terminé ! {len(result)} annonces enregistrées dans annonces.json.")

if __name__ == "__main__":
    main()
