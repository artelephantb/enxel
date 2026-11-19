let mode = 'light';

function switchMode() {
	if (mode == 'dark') {
		document.querySelector('body').style.backgroundColor = '#ffffff';
		Array.from(document.getElementsByTagName('p')).forEach(el => {
			el.style.color = 'black';
		});
		mode = 'light';
	} else {
		document.querySelector('body').style.backgroundColor = '#010016';
		Array.from(document.getElementsByTagName('p')).forEach(el => {
			el.style.color = 'white';
		});
		mode = 'dark';
	}
}
