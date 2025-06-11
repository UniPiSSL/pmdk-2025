
var fs = require('fs');
var crypto = require('crypto');

function encryptFlag(flag, key) {
	const iv = crypto.randomBytes(12);
	const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
	let encrypted = cipher.update(flag, 'utf8', 'base64');
	encrypted += cipher.final('base64');
	const authTag = cipher.getAuthTag();
	return { encrypted, iv: iv.toString('base64'), authTag: authTag.toString('base64') };
}

const plainFlag = fs.readFileSync('./flag.txt', 'utf-8').trim();
const exampleKey = crypto.createHash('sha256').update('nwjs').digest();
const { encrypted, iv, authTag } = encryptFlag(plainFlag, exampleKey);
fs.writeFileSync('encrypted_flag.txt', JSON.stringify({ encrypted, iv, authTag }));
