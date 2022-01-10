// clickEvent Save Bet
$(".valuebetActions span.saveBet").on("click", function () {

    var parentTableData = this.parentElement.parentElement;
  
    parentTableData.classList.toggle("active");
  
  });


// clickEvent Save Bet (mobile)
$(".mobile.betButtons span.saveBet").on("click", function () {

  var betButtonsDiv = this.parentElement.parentElement;

  betButtonsDiv.classList.toggle("active");

});

// clickEvent Cancel bet Bet (mobile)
$(".mobile.betButtons i.cancelBet").on("click", function () {

  var betButtonsDiv = this.parentElement.parentElement;

  betButtonsDiv.classList.toggle("active");

});