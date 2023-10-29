function saveProfile() {
    // Get values from input fields
    var firstName = document.getElementById("firstName").value;
    var lastName = document.getElementById("lastName").value;
    var username = document.getElementById("username").value;
    var bio = document.getElementById("bio").value;

    // Save the profile data (you can send it to a server here)
    // For example: Send an AJAX request to save the data

    alert("Profile saved!");
}

document.getElementById("avatarInput").addEventListener("change", function(event) {
    var file = event.target.files[0];
    var reader = new FileReader();

    reader.onload = function() {
        document.getElementById("avatarImage").src = reader.result;
    }

    reader.readAsDataURL(file);
});