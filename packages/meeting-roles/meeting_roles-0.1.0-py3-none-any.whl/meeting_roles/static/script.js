var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
            panel.style.display = "none";
        } else {
            panel.style.display = "block";
        }
    });
}
function confirmDelete(personId) {
    var result = window.confirm("Are you sure you want to delete this person?");
    if (result) {
        window.location.href = "/delete_person/" + personId;

    }
}

document.getElementById('delete-last-meeting-btn').addEventListener('click', function(e) {
    var r = confirm("Are you sure you want to delete the last meeting?");
    if (r === false) {
        e.preventDefault(); // Prevent the action if the user clicks "Cancel"
    }
    window.location.href =  "/delete_most_recent_meeting";

});


