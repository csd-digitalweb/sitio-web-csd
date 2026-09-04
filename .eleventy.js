module.exports = function (eleventyConfig) {
  // Archivos compartidos: se copian tal cual a la raíz del sitio construido.
  eleventyConfig.addPassthroughCopy("src/fonts.css");
  eleventyConfig.addPassthroughCopy("src/styles.css");
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy({ "src/assets/logo.png": "favicon.ico" });
  eleventyConfig.addPassthroughCopy({ "src/CNAME": "CNAME" });

  // Panel de administración de Decap CMS (Paso 4). El index.html ya lo
  // procesa Eleventy como plantilla normal; config.yml no es un formato
  // de plantilla reconocido, así que necesita copiarse aparte.
  eleventyConfig.addPassthroughCopy({ "src/admin/config.yml": "admin/config.yml" });

  // Fecha legible en español para las noticias: "6 de agosto de 2026".
  const MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
  ];
  eleventyConfig.addFilter("fechaLegible", (fecha) => {
    const d = new Date(fecha);
    return `${d.getUTCDate()} de ${MESES[d.getUTCMonth()]} de ${d.getUTCFullYear()}`;
  });

  // Filtra una colección dejando solo las entradas marcadas "Publicado"
  // desde el panel — así el listado de Noticias nunca muestra borradores.
  eleventyConfig.addFilter("publicados", (items) =>
    (items || []).filter((item) => item.data && item.data.publicado)
  );

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
