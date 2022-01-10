// Disable first element of select item
$(document).ready(function(){

    var selectObj = document.querySelectorAll(".formField select")
    var options = selectObj[0].querySelectorAll("option")
    
    options[0].disabled = true

    var bookieData = document.querySelector(".formCard.addBookie").dataset.userBookies;
    var bookieList = bookieData.split("+");

    for (var i=0; i<options.length; i++){
        var option = options[i];
        var optionValue = option.value.toString()

        if (bookieList.includes(optionValue)) {
            option.disabled = true;
            option.classList.add("disabled")
        };
    }

});