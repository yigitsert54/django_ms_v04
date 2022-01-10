$(document).ready(function(){

    var allopenBetRows = document.querySelectorAll(".bookieBetsSection.myBetsPage table tr.open")

    for (var i=0; i<allopenBetRows.length; i++){
        openBetsRow = allopenBetRows[i]
    
        var rowHeight = openBetsRow.clientHeight;
    
        var matchup = openBetsRow.querySelector("p.matchup");
        var matchupTd = matchup.parentElement;
        var topDownPadding = (99.2-rowHeight) / 2;
    
        topDownPadding = Math.floor(topDownPadding)
    
        matchupTd.style.paddingTop = topDownPadding.toString() + "px"
        matchupTd.style.paddingBottom = topDownPadding.toString() + "px"
    }

});

