$(document).ready(function(){

    var resetEmailField = document.querySelector(".loginForm div.resetEmail input#id_email");
    var pwReset1 = document.querySelector(".loginForm div.resetEmail input#id_new_password1");
    var pwReset2 = document.querySelector(".loginForm div.resetEmail input#id_new_password2");

    

    if(resetEmailField){
        resetEmailField.placeholder = 'E-Mail Adresse';
    }

    if(pwReset1){
        pwReset1.placeholder = 'Neues Passwort';
    }

    if(pwReset2){
        pwReset2.placeholder = 'Neses Passwort bestätigen';
    }

});

$("main .mainContent .loginForm input.formInput").on("input", function () {

    if (this.type == "text"){
        this.value = this.value.toLowerCase();
    };

  });