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
	var activeTab = document.querySelector(".tab[id='" + sectionId + "']");
	activeTab.classList.add("active");
}

function showSubtab(subtabId) {
	// Hide all subtabs
	var subtabs = document.getElementsByTagName("subtab");
	for (var i = 0; i < subtabs.length; i++) {
		subtabs[i].style.display = "none";
	}
	// Show the selected section
	var subtab = document.getElementById(subtabId + "_subtab");
	subtab.style.display = "block";
	// Set the active minitab button
	var subtabbtns = document.getElementsByClassName("subtabbtn");
	for (var i = 0; i < subtabbtns.length; i++) {
		subtabbtns[i].classList.remove("active");
	}
	var activeTab = document.querySelector(".subtabbtn[id='" + subtabId + "']");
	activeTab.classList.add("active");
}

function test() {
	alert("test")
}
