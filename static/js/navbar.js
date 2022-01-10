// toggle dropdown container
$(".headerMenu.desktop .navItem.hasDropdown").on("click", function () {

    var dropdownContainer = this.querySelector("ul.dropdown")

    // toggle dropdown Menu to
    dropdownContainer.classList.toggle("active");

  });

  
// close dropdown on any click on any spot
$(document).on("click", function (event) {

  // get clicked element
  var clickedElement = event.target;

  // if clicked element is the navlink
  if (clickedElement.classList.value.includes("navLink")){

    // element with ".hasDropdown" is 1st level parent
    var parentElement = clickedElement.parentElement

    // Get dropdown container of clicked element
    var clickedContainer = parentElement.querySelector("ul.dropdown")
  }

  // if clicked element is the arrow
  else if (clickedElement.classList.value.includes("dropdownArrow")){

    // element with ".hasDropdown" is 2nd level parent
    var parentElement = clickedElement.parentElement.parentElement

    // Get dropdown container of clicked element
    var clickedContainer = parentElement.querySelector("ul.dropdown")
  }

  // Get all dropdown containers
  var allDropdownContainers = document.querySelectorAll("ul.dropdown")

  // Loop throgh all dropdown containers
  for (var i=0; i<allDropdownContainers.length; i++){

    // Get current dropdown container in the loop
    var container = allDropdownContainers[i]
    
    // remove ".avtive" from all dropdown containers except from the clicked one
    if (container != clickedContainer){
      container.classList.remove("active")
    }
  }
});

// toggle mobile nav container
$("header div.mobileNavLines").on("click", function () {

  var mobileNavContainer = document.querySelector("div.mobileNavContainer");
  var allNavLines = document.querySelectorAll("div.mobileNavLines .navLine");
  
  for (var i=0; i<allNavLines.length; i++){

    // Get current navLine in the loop
    var navLine = allNavLines[i];
    
    // toggle active class in navLine
    navLine.classList.toggle("active");
  }

  // toggle dropdown Menu to
  mobileNavContainer.classList.toggle("active");

});

// toggle submenu items in mobile nav container
$(".headerMenu.mobile .navItem.hasDropdown p").on("click", function () {

  var dropdownContainer = this.parentElement.querySelector("ul.dropdown")

  // toggle dropdown Menu to
  dropdownContainer.classList.toggle("closed");

});
