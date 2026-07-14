import { API_HOST, STORAGE_KEYS } from "./config.js";

chrome.runtime.onInstalled.addListener(async () => {
  const values = await chrome.storage.local.get(STORAGE_KEYS.enabled);
  if (values[STORAGE_KEYS.enabled] === undefined) {
    await chrome.storage.local.set({ [STORAGE_KEYS.enabled]: true });
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message?.type === "BLANKER_ANALYZE_PAGE") {
    analyzePage(message.payload)
      .then((result) => sendResponse({ ok: true, result }))
      .catch((error) => sendResponse({ ok: false, error: error.message }));
    return true;
  }

  return false;
});

async function analyzePage(payload) {
  const values = await chrome.storage.local.get(STORAGE_KEYS.accessToken);
  const accessToken = values[STORAGE_KEYS.accessToken];
  if (!accessToken) {
    throw new Error("Access token is not configured.");
  }

  const response = await fetch(`${API_HOST}/api/analysis-requests`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${accessToken}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  const body = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(body?.error?.message || body?.message || "Analysis request failed.");
  }

  return body;
}
