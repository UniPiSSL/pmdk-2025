
const terminal = new Terminal();
terminal.open(document.getElementById('terminal'));

process.mainModule.exports.bindTerminal(terminal);
