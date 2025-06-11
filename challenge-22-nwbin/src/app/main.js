
var fs = require('fs');
var crypto = require('crypto');
var readline = require('readline');


function hash(input, type='hex') {
	return crypto.createHash('sha256').update(input).digest('hex');
}

function decryptFlag(encrypted, key, iv, authTag) {
	const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
	decipher.setAuthTag(authTag);
	let decrypted = decipher.update(encrypted, 'base64', 'utf8');
	decrypted += decipher.final('utf8');
	return decrypted;
}

/*
function encryptFlag(flag, key) {
	const iv = crypto.randomBytes(12);
	const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
	let encrypted = cipher.update(flag, 'utf8', 'base64');
	encrypted += cipher.final('base64');
	const authTag = cipher.getAuthTag();
	return { encrypted, iv: iv.toString('base64'), authTag: authTag.toString('base64') };
}
*/

exports.bindTerminal = function(term){
	term.focus();
	var debug = false;

	// Read the encrypted flag from file
	var { encrypted, iv, authTag } = JSON.parse(fs.readFileSync('./encrypted_flag.txt', 'utf-8'));

	term.write(
		'I live where JavaScript meets Chromium’s might,' + '\r\n' +
		'In a package of wonders, I hide out of sight.' + '\r\n' +
		'I’m not a browser, yet I wield the same tools,' + '\r\n' +
		'My local file powers defy the old rules.' + '\r\n' +
		'' + '\r\n' +
		'My secrets lie deep in JSON and code,' + '\r\n' +
		'Where scripts and configs reveal what’s bestowed.' + '\r\n' +
		'To uncover my truths, decompile and explore,' + '\r\n' +
		'Crack open my heart to unlock what’s in store.' + '\r\n' +
		'' + '\r\n'
	);

	const wait4input = [];

	const handleInput = function(buffer) {
		while (wait4input.length > 0) {
			(wait4input.shift())(buffer);
		}
	}

	// Handle new lines
	var term_buffer = '';

	term.onData((data) => {
		const char = data;
		if (char == '\n' || char == '\r') {
			term.write('\r\n');
			handleInput(term_buffer);
			term_buffer = '';
		}
		else if (char === '\u007F') {
			if (term_buffer.length > 0) {
				term_buffer = term_buffer.slice(0, -1);
				term.write('\b \b');
			}
		}
		else {
			term_buffer += char;
			term.write(char);
		}
	});

	const question = function(ask, callback) {
		term.focus();
		term.write(ask);
		wait4input.push(callback);
	}

	// Prompt user for input
	question('Who am I? ', (userInput) => {
		var key = userInput.toLowerCase().replace(/[^a-z]+/g, '').trim();
		var input_hash = hash(key);
		if (input_hash === '0e54775fef09e53533c4de9aa6cfbf3ade7fb444f85d2dbd41d4b421c9621058') {
			term.write('Correct!\r\n');
			if (debug) {
				var flag = decryptFlag(
					encrypted,
					crypto.createHash('sha256').update(key).digest(),
					Buffer.from(iv, 'base64'),
					Buffer.from(authTag, 'base64')
				);
				term.write(`${flag}\r\n`);
				term.write('\r\n');
				return;
			}
		}
		else if (input_hash === '88b1deea6a18cfd0d1df1f0048d0946332fe61d1adc2bacb25e5f6a774b56cc5') {
			term.write('Nop! But you are close...\r\n');
		}
		else {
			term.write('Nop... Try again...\r\n');
		}
		setTimeout(function(){
			process.exit(0);
		}, 1000);
	});
};
