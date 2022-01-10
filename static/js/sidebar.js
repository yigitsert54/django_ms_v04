// Add .openSubmenu to dropdown
$(".dropdownNavlink .navLink").on("click", function () {

    // toggle openSubmenu to dropdownNavlink element
    this.parentElement.classList.toggle("openSubmenu");
  
    // get submenuContainer of clicked dropdownNavlink
    submenuContainer = this.parentElement.querySelector(".submenuContainer");
  
    // open submenu animation
    openSubmenu(submenuContainer);
  
  });
  
  // submenu animation (get right max-height of submenuContainer)
  function openSubmenu(submenuContainer){
    // get a list of all submenus of clicked dropdownNavlink
    allSubsList = submenuContainer.querySelectorAll(".navLink.submenu");
  
    // extract how many submenu elements a dropdown has got
    subAmount = allSubsList.length;
  
    // extract overall navlink height
    navHeight = allSubsList[0].clientHeight;
    
    // if submenu is closed (height = 0), increase height to fit number of elements (subAmount * navHeight)
    if (submenuContainer.clientHeight == 0) {
        submenuContainer.style.maxHeight = (subAmount * navHeight).toString() +"px";
    } 
    // [else] if submenu is open (height > 0), set height to 0
    else {
        submenuContainer.style.maxHeight = "0px";
    }
  }
  
  // // Sidebar Toggler
  // $("i.sidebarToggler").on("click", function () {
  
  //     // get sidebar element
  //     sidebar = document.querySelector(".sidebar")
    
  //     // toggle "close" on sidebar element
  //     sidebar.classList.toggle("close");
  //     sidebar.classList.toggle("closeFix");
  
  //   });
  
  // // Open sidebar on hover
  // $(".sidebar").on("mouseover", function () {
  
  //     // get sidebar element
  //     sidebar = document.querySelector(".sidebar")
  
  //     if (sidebar.classList.value.includes("close")){
  //         console.log("close in sidebar")
  
  //         // toggle "close" on sidebar element
  //         sidebar.classList.toggle("close");
  //     }
  
  
  //   });
  
  // // Close side
  // $(".sidebar").on("mouseout", function () {
  
  //     // get sidebar element
  //     sidebar = document.querySelector(".sidebar")
  
  //     if (sidebar.classList.value.includes("closeFix")){
  
  //         // toggle "close" on sidebar element
  //         sidebar.classList.toggle("close");
  //     }
  
  
  //   });