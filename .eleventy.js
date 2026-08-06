module.exports = function (eleventyConfig) {
  // Archivos compartidos: se copian tal cual a la raíz del sitio construido.
  eleventyConfig.addPassthroughCopy("src/fonts.css");
  eleventyConfig.addPassthroughCopy("src/styles.css");
  eleventyConfig.addPassthroughCopy("src/assets");

  // Fecha legible en español para las noticias: "6 de agosto de 2026".
  const MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
  ];
  eleventyConfig.addFilter("fechaLegible", (fecha) => {
    const d = new Date(fecha);
    return `${d.getUTCDate()} de ${MESES[d.getUTCMonth()]} de ${d.getUTCFullYear()}`;
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
  };
};
