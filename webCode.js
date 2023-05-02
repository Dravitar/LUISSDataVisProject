function showSection(sectionId) {
	// Hide all sections
	var sections = document.getElementsByTagName("section");
	for (var i = 0; i < sections.length; i++) {
		sections[i].style.display = "none";
	}
	// Show the selected section
	var section = document.getElementById(sectionId + "_section");
	section.style.display = "block";
	// Set the active tab button
	var tabs = document.getElementsByClassName("tab");
	for (var i = 0; i < tabs.length; i++) {
		tabs[i].classList.remove("active");
	}
	var activeTab = document.querySelector(".tab[data-section='" + sectionId + "']");
	activeTab.classList.add("active");
}

function test() {
	alert("test")
}
