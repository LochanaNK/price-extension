document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("productUrl");
  const fetchBtn = document.getElementById("fetchPrice");
  const resultsDiv = document.getElementById("results");

  const BACKEND_URL = "https://price-extension.fly.dev/";

  // Sanitize URL to remove unnecessary query params
  function sanitizeUrl(url) {
    try {
      const parsed = new URL(url);
      return parsed.origin + parsed.pathname;
    } catch {
      return url;
    }
  }

  // Display results from backend
  function displayResults(items) {
    if (!items || items.length === 0) {
      resultsDiv.innerHTML = "<p>No products found</p>";
      return;
    }

    resultsDiv.innerHTML = items.map(item => `
      <div>
        <p><strong>Platform:</strong> ${item.platform}</p>
        <p><strong>Title:</strong> ${item.title || item.name}</p>
        <p><strong>Price:</strong> ${item.price}</p>
        <p><strong>Link:</strong> <a href="${item.link}" target="_blank">${item.link}</a></p>
      </div>
    `).join("");
  }

  // Fetch price comparison from backend
  async function fetchPrice(url) {
    const sanitized = sanitizeUrl(url);

    // Determine the other platform to compare
    let compareUrl = sanitized;
    if (sanitized.includes("aliexpress.com")) {
      compareUrl = `${sanitized},daraz_search_placeholder`;
    } else if (sanitized.includes("daraz.lk")) {
      compareUrl = `${sanitized},aliexpress_search_placeholder`; 
    }

    try {
      const response = await fetch(`${BACKEND_URL}/compare?urls=${encodeURIComponent(compareUrl)}`);
      const data = await response.json();
      displayResults(data);
    } catch (err) {
      console.error(err);
      resultsDiv.innerHTML = `<p style="color:red">Error fetching price</p>`;
    }
  }


  fetchBtn.addEventListener("click", () => {
    const url = input.value.trim();
    if (url) fetchPrice(url);
  });
});
