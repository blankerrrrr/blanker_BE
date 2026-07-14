import { STORAGE_KEYS } from "./config.js";

const enabledInput = document.querySelector("#enabled");
const accessTokenInput = document.querySelector("#accessToken");
const saveTokenButton = document.querySelector("#saveToken");
const analyzePageButton = document.querySelector("#analyzePage");
const statusText = document.querySelector("#status");

init();

async function init() {
  const values = await chrome.storage.local.get([
    STORAGE_KEYS.accessToken,
    STORAGE_KEYS.enabled
  ]);

  enabledInput.checked = values[STORAGE_KEYS.enabled] !== false;
  accessTokenInput.value = values[STORAGE_KEYS.accessToken] || "";

  enabledInput.addEventListener("change", saveEnabled);
  saveTokenButton.addEventListener("click", saveAccessToken);
  analyzePageButton.addEventListener("click", analyzeCurrentPage);
}

async function saveEnabled() {
  await chrome.storage.local.set({
    [STORAGE_KEYS.enabled]: enabledInput.checked
  });
  setStatus("Saved.");
}

async function saveAccessToken() {
  await chrome.storage.local.set({
    [STORAGE_KEYS.accessToken]: accessTokenInput.value.trim()
  });
  setStatus("Token saved.");
}

async function analyzeCurrentPage() {
  setBusy(true);
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab?.id) {
      throw new Error("Active tab not found.");
    }

    const collected = await chrome.tabs.sendMessage(tab.id, {
      type: "BLANKER_COLLECT_PAGE"
    });
    if (!collected?.contents?.length) {
      throw new Error("No page content collected.");
    }

    const response = await chrome.runtime.sendMessage({
      type: "BLANKER_ANALYZE_PAGE",
      payload: collected
    });
    if (!response?.ok) {
      throw new Error(response?.error || "Analysis failed.");
    }

    setStatus("Analysis completed.");
  } catch (error) {
    setStatus(error.message);
  } finally {
    setBusy(false);
  }
}

function setBusy(isBusy) {
  analyzePageButton.disabled = isBusy;
  saveTokenButton.disabled = isBusy;
}

function setStatus(message) {
  statusText.textContent = message;
}
