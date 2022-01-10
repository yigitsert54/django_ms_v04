// toggle faq accordion
$("main div.faqCard").on("click", function () {

    // Get the answer element
    var answerElement = this.querySelector("div.answer p");

    // Check if height of the answer div is greater than 0
    if (answerElement.parentElement.clientHeight > 0){

        // if yes set it to 0
        answerElement.parentElement.style.maxHeight = "0px"

    } else{

        // if no expand the answer div to its content height
        answerElement.parentElement.style.maxHeight = answerElement.clientHeight.toString() + "px";

    }

    this.classList.toggle("show")

  });


// clickEvent for topicCard
$(".topicCard").on("click", function () {

    // Get bookie url from data-bookieUrl
    url = this.dataset.topicUrl;
  
    window.location = url;
  
  });