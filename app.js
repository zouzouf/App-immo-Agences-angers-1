// Remplace cette URL par le lien vers ton fichier JSON généré par ton serveur tiers (ex: GitHub Gist ou serveur Render)
const API_URL = "https://raw.githubusercontent.com/ton-compte/ton-repo/main/annonces.json";

// Données de démonstration (utilisées si l'API_URL n'est pas encore prête)
const DEMO_DATA = [
  {
    id: 1,
    title: "Appartement T2 quartier Doutre",
    price: 118000,
    agency: "Blot Immobilier",
    description: "Ideal investisseur ou premier achat. T2 de 38m² proche des commerces et des transports.",
    url: "https://www.blot-immobilier.fr"
  },
  {
    id: 2,
    title: "Studio lumineux Ney / Chalouère",
    price: 95000,
    agency: "Square Habitat",
    description: "Studio de 24m² entièrement rénové au 2ème étage d'une petite copropriété.",
    url: "https://www.squarehabitat.fr"
  },
  {
    id: 3,
    title: "T2 avec balcon - Lac de Maine",
    price: 124500,
    agency: "Nicole Joubert",
    description: "Au calme, appartement comprenant entrée, séjour sur balcon, cuisine indépendante et chambre.",
    url: "https://www.nicolejoubert.fr"
  }
];

let allListings = [];

const container = document.getElementById("listings-container");
const agencySelect = document.getElementById("agency-select");
const statusMessage = document.getElementById("status-message");
const refreshBtn = document.getElementById("refresh-btn");

async function fetchListings() {
  statusMessage.textContent = "Recherche des annonces en cours...";
  try {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error("API non disponible");
    allListings = await response.json();
    statusMessage.textContent = "";
  } catch (err) {
    console.warn("Erreur chargement API, passage aux données de démonstration.");
    allListings = DEMO_DATA;
    statusMessage.textContent = "Mode Démo (Serveur non connecté)";
  }

  // Filtrer strictement < 125 000 €
  allListings = allListings.filter(item => item.price < 125000);

  populateAgencyFilter();
  renderListings(allListings);
}

function populateAgencyFilter() {
  const agencies = [...new Set(allListings.map(item => item.agency))];
  agencySelect.innerHTML = '<option value="all">Toutes les agences</option>';
  agencies.forEach(agency => {
    const option = document.createElement("option");
    option.value = agency;
    option.textContent = agency;
    agencySelect.appendChild(option);
  });
}

function renderListings(items) {
  container.innerHTML = "";
  if (items.length === 0) {
    container.innerHTML = "<p>Aucune annonce trouvée pour ce critère.</p>";
    return;
  }

  items.forEach(item => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <div class="card-header">
        <h2 class="card-title">${item.title}</h2>
        <span class="card-price">${item.price.toLocaleString("fr-FR")} €</span>
      </div>
      <span class="card-agency">${item.agency}</span>
      <p class="card-desc">${item.description}</p>
      <a href="${item.url}" target="_blank" class="card-link">Voir l'annonce complète ↗</a>
    `;
    container.appendChild(card);
  });
}

agencySelect.addEventListener("change", (e) => {
  const selected = e.target.value;
  if (selected === "all") {
    renderListings(allListings);
  } else {
    const filtered = allListings.filter(item => item.agency === selected);
    renderListings(filtered);
  }
});

refreshBtn.addEventListener("click", fetchListings);

// Premier chargement
fetchListings();
