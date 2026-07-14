const MAX_TEXT_LENGTH = 5000;

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message?.type !== "BLANKER_COLLECT_PAGE") {
    return false;
  }

  sendResponse({
    page: {
      url: window.location.href,
      title: document.title || null
    },
    contents: collectTextContents()
  });
  return false;
});

function collectTextContents() {
  const mainText = document.body?.innerText?.trim() || "";
  const text = mainText.slice(0, MAX_TEXT_LENGTH);

  if (!text) {
    return [];
  }

  return [
    {
      clientContentId: "page_body",
      unitType: "TEXT",
      text,
      contextText: document.title || null,
      selector: "body"
    }
  ];
}
