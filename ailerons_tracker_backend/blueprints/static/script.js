const header = document.getElementById("navbar");

function debounce(func, timeout = 200) {
	let timer;
	return (...args) => {
		clearTimeout(timer);
		timer = setTimeout(() => {
			func.apply(this, args);
		}, timeout);
	};
}

function saveInput() {
	console.log("Saving data");
}

const handlePointerEvents = debounce((e) => {
	let position = e.clientY;
	console.log("pos1", position);

	if (position < 160) {
		header.classList.add("show", true);
	} else {
		if (header.classList.contains("show"))
			header.classList.toggle("show", false);
	}
});

window.onmousemove = (e) => {
	handlePointerEvents(e);
};
