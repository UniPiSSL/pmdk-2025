<?php

function getCart() {
	return isset($_SESSION['cart']) ? $_SESSION['cart'] : [];
}

function clearCart() {
	$_SESSION['cart'] = [];
}

function addToCart($itemId, $quantity) {
	// Initialize cart if not already
	if (!isset($_SESSION['cart'])) {
		$_SESSION['cart'] = [];
	}

	//// Add or update item in cart
	//if (isset($_SESSION['cart'][$itemId])) {
	//	$_SESSION['cart'][$itemId] += $quantity;
	//} else {
	//	$_SESSION['cart'][$itemId] = $quantity;
	//}

	if ($quantity > 0) {
		$_SESSION['cart'][$itemId] = $quantity;
	}
	else {
		unset($_SESSION['cart'][$itemId]);
	}
}

function calculateTotal($items, $prices) {
	$total = 0;
	foreach ($items as $itemId => $quantity) {
		$total += $prices[$itemId] * $quantity;
	}
	return $total;
}

function calculateTax($total, $taxRate = 0.24) {
	return $total * $taxRate;
}

function getDonuts($searchQuery = '') {
	global $app_db;
	$query = "SELECT * FROM donuts";
	
	// Add search filter if a search query is provided
	if (!empty($searchQuery)) {
		$query .= " WHERE name LIKE '%$searchQuery%'";
	}
	$query .= " ORDER BY name DESC";

	$result = $app_db->query($query);

	$donuts = [];
	while ($row = $result->fetchArray()) {
		$donuts[] = $row;
	}

	return $donuts;
}

function getOrders() {
	global $app_db;
	$query = "SELECT * FROM orders ORDER BY id ASC";
	$result = $app_db->query($query);

	$orders = [];
	while ($row = $result->fetchArray()) {
		$orders[] = $row;
	}

	return $orders;
}

function deleteOrder($orderId) {
	global $app_db;
	$app_db->exec("DELETE FROM orders WHERE id = '$orderId'");
}

function saveOrderToDatabase($items, $totalWithTax, $name) {
	global $app_db;
	$orderItems = json_encode($items);
	$app_db->exec("INSERT INTO orders (items, total, name) VALUES ('$orderItems', '$totalWithTax', '$name')");
}

function verifyCredentials($username, $password) {
	global $app_db;

	$stmt = $app_db->prepare("SELECT password FROM admins WHERE username = :username");
	$stmt->bindValue(':username', $username, SQLITE3_TEXT);
	$result = $stmt->execute();

	if ($user = $result->fetchArray(SQLITE3_ASSOC)) {
		if ($password === $user['password']) {
			return true;
		}
	}

	return false;
}
