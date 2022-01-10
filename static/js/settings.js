$(document).ready(function(){

    var oldPassword = document.querySelector(".changePassword #id_old_password")
    var newPassword1 = document.querySelector(".changePassword #id_new_password1")
    var newPassword2 = document.querySelector(".changePassword #id_new_password2")

    oldPassword.placeholder = "Aktuelles Passwort eingeben"
    newPassword1.placeholder = "Neues Passwort eingeben"
    newPassword2.placeholder = "Neues Passwort bestätigen"

});