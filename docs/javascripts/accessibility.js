document.addEventListener("DOMContentLoaded", () => {
  const tables = document.querySelectorAll(".md-typeset table:not([role])");
  tables.forEach((t) => t.setAttribute("role", "table"));
});
