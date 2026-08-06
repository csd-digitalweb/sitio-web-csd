module.exports = {
  layout: "noticia.njk",
  tags: ["noticias"],
  eleventyComputed: {
    // Título que va en la pestaña del navegador y en Google — el campo
    // "title" que llena la persona en el panel se queda limpio, sin repetir
    // "Colegio CSD" cada vez.
    pageTitle: (data) => `${data.title} — Colegio CSD`,
  },
};
