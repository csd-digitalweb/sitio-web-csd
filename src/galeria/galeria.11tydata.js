module.exports = {
  layout: "album.njk",
  tags: ["galeria"],
  eleventyComputed: {
    pageTitle: (data) => `${data.title} — Colegio CSD`,
  },
};
