<?php

include_once('includes/app.php');
include_once('includes/functions.php');

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
	$itemId = $_POST['id'];
	$quantity = (int) $_POST['quantity'];
	
	$item = NULL;
	$donuts = getDonuts();
	foreach ($donuts as $donut) {
		if ($donut['id'] == $itemId) {
			$item = $donut;
			break;
		}
	}
	
	// Add to cart using helper function
	if ($item) {
		addToCart($donut['id'], $quantity);
	}
}

// Redirect to eat.php
header('Location: eat.php');
