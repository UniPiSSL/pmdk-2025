/*
	Defacer js code by
	anD_th3_3Rd_paRT3_IN_Js}
*/
let glitched = [... document.querySelectorAll('.glitch')];
glitched.forEach(g => {
	if (g.dataset.text) {
		for (let i = 9; i >= 0; i--) {
			let div = document.createElement('div');
			div.className = 'line';
			div.textContent = g.dataset.text;
			g.appendChild(div);
		}
	}
});
