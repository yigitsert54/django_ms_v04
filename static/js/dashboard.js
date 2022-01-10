var performanceCard = document.querySelector("main .performanceBookieSection .performanceCard")
var bookieCard = document.querySelector("main .performanceBookieSection .bookieCard")

performanceWidth = bookieCard.clientWidth / performanceCard.clientWidth

$(window).on('resize', function(){
  var performanceCard = document.querySelector("main .performanceBookieSection .performanceCard")
  var bookieCard = document.querySelector("main .performanceBookieSection .bookieCard")

  finalWidth = bookieCard.clientWidth * performanceWidth

  performanceCard.style.maxWidth = finalWidth.toString() + "px"
});