// Page furniture that CSS cannot draw: the full-bleed header band
// (MANUAL-STYLE-GUIDE.md §2.2) on every page except the cover.
class SummitPushFurniture extends Paged.Handler {
  afterPageLayout(pageElement) {
    if (pageElement.classList.contains("pagedjs_cover_page")) return;
    const sheet = pageElement.querySelector(".pagedjs_sheet");
    const band = document.createElement("div");
    band.className = "band";
    band.innerHTML =
      '<span class="band-mark">SUMMIT PUSH</span>' +
      '<span class="band-rule"></span>' +
      '<span class="band-title">SUMMIT PUSH — Game Manual</span>';
    sheet.appendChild(band);
  }
}
Paged.registerHandlers(SummitPushFurniture);

// A table that runs onto another page repeats its header row there (MANUAL-STYLE-GUIDE.md §2.4).
// Paged.js rebuilds the table around the first row it carries over, marked data-split-from,
// without the <thead>; copy the source table's header in before the rows are measured.
class SummitPushTableHeaders extends Paged.Handler {
  renderNode(clone, node) {
    const at = clone.nodeType === 1 ? clone : clone.parentElement;
    const table = at && at.closest("table[data-split-from]");
    if (!table || table.querySelector(":scope > thead")) return;
    const from = node.nodeType === 1 ? node : node.parentElement;
    const head = from && from.closest("table") && from.closest("table").querySelector(":scope > thead");
    if (head) table.insertBefore(head.cloneNode(true), table.firstChild);
  }
}
Paged.registerHandlers(SummitPushTableHeaders);
