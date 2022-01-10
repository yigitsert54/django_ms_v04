$(document).ready(function(){

    var allPaginationBtns = document.querySelectorAll("ul.pagination li a")
    
    for (var i=0; i<allPaginationBtns.length; i++){

        var link = allPaginationBtns[i]
        
        link.href += "#scroll2bets"
      }

});