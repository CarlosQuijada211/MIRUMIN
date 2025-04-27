const sidebar = document.getElementById("sidebar");

function toggleSidebar() {
    sidebar.classList.toggle("show")
}

function toggleSubMenu(button){
    button.nextElementSibling.classList.toggle("show")
}