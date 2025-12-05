const input = document.getElementById("productUrl");
const fetchBtn = document.getElementById("fetchPrice");
const resultsDiv = document.getElementById("results");

const BACKEND_URL = "https://price-extension.fly.dev/";

async function fetchPrice(url) {
  try {
    // Call the compare endpoint instead of scrape
    const response = await fetch(`${BACKEND_URL}/compare?url=${encodeURIComponent(url)}`);
    const data = await response.json();
    displayResults(data);
  } catch (err) {
    console.error(err);
    resultsDiv.innerHTML = `<p style="color:red">Error fetching price</p>`;
  }
}

function displayResults(items) {
  if (!items || items.length === 0) {
    resultsDiv.innerHTML = "<p>No products found</p>";
    return;
  }

  resultsDiv.innerHTML = items.map(item => `
    <div style="margin-bottom:1em;">
      <p><strong>Platform:</strong> ${item.platform}</p>
      <p><strong>Title:</strong> ${item.title || item.name}</p>
      <p><strong>Price:</strong> ${item.price}</p>
      <p><strong>Link:</strong> <a href="${item.link}" target="_blank">${item.link}</a></p>
    </div>
  `).join("");
}

function sanitizeUrl(url) {
  try {
    const parsed = new URL(url);

    return parsed.origin + parsed.pathname;
  } catch {
    return url; 
  }
}

fetchBtn.addEventListener("click", () => {
  const url = input.value.trim();
  if (url) fetchPrice(url);
});
