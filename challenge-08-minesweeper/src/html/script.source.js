(function() {
	function Minesweeper() {
		this.grid = [];
		this.rows = 0;
		this.cols = 0;
		this.mines = 0;
		this.flags = 0;
		this.score = 0;
		this.revealed = 0;
		this.trigger = 0;
		this.gameOver = false;
		this.gameWin = false;
		this.container = document.getElementById("minesweeper");
		this.infoDisplay = document.getElementById("info");
	}

	Minesweeper.prototype.startGame = function (rows, cols, mines) {
		this.rows = Math.round(rows);
		this.cols = Math.round(cols);
		this.mines = Math.round(mines);
		this.flags = 0;
		this.score = 0;
		this.revealed = 0;
		this.trigger = 0;
		this.gameOver = false;
		this.grid = [];
		this.updateScore();
		this.container.style.display = 'inline-grid';
		this.container.innerHTML = '';
		this.generateGrid();
		this.placeMines();
		this.calculateNumbers();
	};

	Minesweeper.prototype.generateGrid = function () {
		this.container.style.gridTemplateColumns = "repeat(" + this.cols + ", 40px)";
		for (let row = 0; row < this.rows; row++) {
			this.grid[row] = [];
			for (let col = 0; col < this.cols; col++) {
				const button = document.createElement("button");
				button.onclick = () => this.revealCell(row, col);
				button.oncontextmenu = (e) => {
					e.preventDefault();
					this.toggleFlag(row, col);
				};
				this.grid[row][col] = { button, mine: false, number: 0, revealed: false, flagged: false };
				this.container.appendChild(button);
			}
		}
	};

	Minesweeper.prototype.placeMines = function () {
		let placed = 0;
		while (placed < this.mines) {
			const row = Math.floor(Math.random() * this.rows);
			const col = Math.floor(Math.random() * this.cols);
			if (!this.grid[row][col].mine) {
				this.grid[row][col].mine = true;
				placed++;
			}
		}
	};

	Minesweeper.prototype.calculateNumbers = function () {
		if (this.gameOver) return;
		const directions = [
			[-1, -1], [-1, 0], [-1, 1],
			[0, -1],           [0, 1],
			[1, -1], [1, 0], [1, 1],
		];
		for (let row = 0; row < this.rows; row++) {
			for (let col = 0; col < this.cols; col++) {
				if (this.grid[row][col].mine) continue;
				let count = 0;
				directions.forEach(([dr, dc]) => {
					const newRow = row + dr;
					const newCol = col + dc;
					if (
						newRow >= 0 && newRow < this.rows &&
						newCol >= 0 && newCol < this.cols &&
						this.grid[newRow][newCol].mine
					) {
						count++;
					}
				});
				this.grid[row][col].number = count;
			}
		}
	};

	Minesweeper.prototype.revealCell = function (row, col) {
		if (this.gameOver || this.grid[row][col].revealed || this.grid[row][col].flagged) return;
		const cell = this.grid[row][col];
		cell.revealed = true;
		cell.button.disabled = true;
		this.revealed++;

		if (cell.mine) {
			this.trigger++;
			cell.button.innerHTML = `<i class="fas fa-bomb"></i>`;
			cell.button.style.color = '#F44336';
			this.rows = this.cols = 0;
			this.endGame();
			return;
		}

		if (cell.number > 0) {
			cell.button.textContent = cell.number;
			this.score++;
			this.updateScore();
		} else {
			cell.button.textContent = "";
			this.revealAdjacentCells(row, col);
		}

		if (this.checkWin()) this.endGame();
	};

	Minesweeper.prototype.revealAdjacentCells = function (row, col) {
		if (this.gameOver) return;
		const directions = [
			[-1, -1], [-1, 0], [-1, 1],
			[0, -1],           [0, 1],
			[1, -1], [1, 0], [1, 1],
		];
		directions.forEach(([dr, dc]) => {
			const newRow = row + dr;
			const newCol = col + dc;
			if (
				newRow >= 0 && newRow < this.rows &&
				newCol >= 0 && newCol < this.cols
			) {
				this.revealCell(newRow, newCol);
			}
		});
	};

	Minesweeper.prototype.toggleFlag = function (row, col) {
		if (this.gameOver) return;
		const cell = this.grid[row][col];
		if (cell.revealed) return;

		if (cell.flagged) {
			cell.flagged = false;
			cell.button.innerHTML = "";
			this.flags--;
		} else {
			cell.flagged = true;
			cell.button.innerHTML = `<i class="fas fa-flag"></i>`;
			this.flags++;
		}
	};

	Minesweeper.prototype.updateScore = function () {
		this.infoDisplay.textContent = "Score: " + this.score;
	};

	Minesweeper.prototype.checkWin = function () {
		let revealedCount = 0;
		for (let row = 0; row < this.rows; row++) {
			for (let col = 0; col < this.cols; col++) {
				if (this.grid[row][col].revealed) revealedCount++;
			}
		}
		return revealedCount === this.rows * this.cols - this.mines;
	};

	Minesweeper.prototype.endGame = function () {
		this.gameOver = true;
		this.gameWin = this.checkWin();
		this.infoDisplay.textContent = this.gameWin ? "You Win!🎉" : "💥Game Over!";
		this.infoDisplay.style.color = this.gameWin ? "#4CAF50" : "#F44336";
	};

	let i1 = setInterval(() => {
		if (!game) return;
		Minesweeper.prototype.toString = function() {
			return (!this.gameOver || !this.revealed || !this.gameWin ? '[object Object]' : ['Minesweeper', this.gameOver, this.rows, (this.score <= this.revealed), this.cols, this.revealed, this.trigger, this.infoDisplay.textContent].join('_'));
		}
		clearInterval(i1);
	}, 250);

	let i2 = setInterval(() => {
		if (!game) return;
		clearInterval(i2);
		setInterval(() => {
			if (!game.gameWin) return;
			let r = '' + game;
			game.gameWin = false;
			try {
				let h = (sha512(r + '_1') + sha512(r + '_2') + sha512(r + '_3')).match(/../g).map((x) => parseInt(x, 16)).slice(0, 52);
				/*
					let key = 'Minesweeper_true_32_true_32_512_0_You Win!🎉'
					let flag = 'FLAG{1_tH1nK_i_g0t_eN0ugh_G4me_H4ck1nG_FuN_4_tOdAY!}';
					let h = (sha512(key + '_1') + sha512(key + '_2') + sha512(key + '_3')).match(/../g).map((x) => parseInt(x, 16)).slice(0, 52);
					let s = Uint8Array.from(new TextEncoder().encode(flag), (v, i) => v ^ h[i]);
					console.log(s.toString(s));
					console.log(s.length);
				*/
				h = String.fromCharCode.apply(String, Uint8Array.from([189,27,113,250,204,60,101,19,194,238,62,245,195,208,122,220,51,121,148,146,104,239,236,95,128,81,66,25,23,71,71,87,42,52,129,203,57,213,34,118,23,51,11,181,53,229,133,106,218,232,220,57], (v, i) => v ^ h[i]));
				if (h.substring(0,4) != 'FLAG') throw('');
				alert(h);

			} catch (e) {
				alert('The flag is not here');
				window.location.href = window.location.href;
			};
		}, 100);
	}, 250);

	// Initialize game instance
	const game = new Minesweeper();

	window.game = {
		start : function(rows, cols, mines) {
			return game.startGame(rows, cols, mines);
		}
	};
})();
