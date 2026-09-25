// Page furniture that CSS margin boxes cannot draw: the full-bleed header band
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
