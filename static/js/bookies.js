// clickEvent for bookieCard
$(".bookieCard").on("click", function () {

  // Get bookie url from data-bookieUrl
  url = this.dataset.bookieUrl;

  window.location = url;

});
