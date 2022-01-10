// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();
});

var alertWrapper = document.querySelector('.alert');
var alertClose = document.querySelector('.alert__close');

if (alertWrapper) {
  alertClose.addEventListener('click', () =>  
    alertWrapper.style.display = 'none'
  )
};


// $(".alert__close").on('click', function(){

//   this.style.display = 'none';

//   console.log("clicked")

//   var alertWrapper = document.querySelector('.alert');
//   alertWrapper.style.display = 'none';
  
// });