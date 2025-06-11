<?php

// Check if the database file exists
if (!file_exists(WEBSITE_DATABASE_PATH)) {
	// Create empty file
	$handle = fopen(WEBSITE_DATABASE_PATH, 'w');

	// Check if file creation was successful
	if ($handle === false) {
		die('Unable to create the database file.');
	}
	else {
		fclose($handle);
	}
	unset($handle);

	// Init database
	$app_db = new SQLite3(WEBSITE_DATABASE_PATH);

	$app_db->exec('CREATE TABLE IF NOT EXISTS admins (id INTEGER PRIMARY KEY, username TEXT, password TEXT)');
	$app_db->exec('INSERT INTO admins (username, password) VALUES ("admin", "{{RANDOM-ADMIN-PASSWORD}}")');

	$app_db->exec('CREATE TABLE IF NOT EXISTS donuts (id INTEGER PRIMARY KEY, name TEXT, price REAL, image TEXT)');
	$app_db->exec('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, items TEXT, total REAL, name TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)');

	$items = [
		['Plain Sprinkled', 2.00, 'images/donut-simple-sprinkles.png'],
		['Chocolate Glazed', 2.00, 'images/donut-chocolate-plain.png'],
		['Chocolate Biscuit Glazed', 2.50, 'images/donut-chocolate-biscuit.png'],
		['Chocolate Sprinkled', 2.50, 'images/donut-chocolate-sprinkles.png'],
		['Strawberry Glazed', 3.00, 'images/donut-pink-chocolate-extra.png'],
		['Strawberry Sprinkled', 3.50, 'images/donut-pink-chocolate-sprinkles.png'],
		['White Chocolate Glazed', 3.50, 'images/donut-white-chocolate-extra.png'],
		['Caramel Glazed', 3.75, 'images/donut-caramel-plain.png'],
		['Cherry Glazed', 3.75, 'images/donut-cherry-plain.png'],
		['Cherry Sprinkled', 4.00, 'donut-cherry-sprinkles.png'],
		['Red Velvet Sprinkled', 3.75, 'images/donut-red-velvet-sprinkles.png']
	];

	$stmt = $app_db->prepare('INSERT INTO donuts (name, price, image) VALUES (:name, :price, :image)');
	foreach ($items as $item) {
		$stmt->bindParam(':name', $item[0], SQLITE3_TEXT);
		$stmt->bindParam(':price', $item[1], SQLITE3_FLOAT);
		$stmt->bindParam(':image', $item[2], SQLITE3_TEXT);
		$stmt->execute();
	}
	unset($items);
	unset($stmt);
}
else {
	$app_db = new SQLite3(WEBSITE_DATABASE_PATH);
}
