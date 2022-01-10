// close message event
$("div.messageSektion p i.close").on("click", function () {

    var allMessageSections = document.querySelectorAll("div.messageSektion");

    for (var i=0; i<allMessageSections.length; i++){

        // Get current messageSection in the loop
        var messageSection = allMessageSections[i]
        
        messageSection.classList.add("close")
      }
  
  });