<?php

include_once('includes/app.php');
include_once('includes/functions.php');

// Retrieve donuts data
$donuts = getDonuts();

// Get cart items
$cart = getCart();

// Initialize total cost
$total = 0;

// Calculate total price of items in the cart
foreach ($cart as $itemId => $quantity) {
	foreach ($donuts as $donut) {
		if ($donut['id'] == $itemId) {
			$total += $donut['price'] * $quantity;
		}
	}
}

// Calculate tax (24%)
$tax = calculateTax($total, 0.24);
$totalWithTax = $total + $tax;

// Handle order submission
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
	// Get name for the order
	$name = trim(preg_replace("/[^A-Za-z0-9 ]/", '', $_POST['name']));

	// Save the order to the database
	saveOrderToDatabase($cart, $totalWithTax, $name);
	
	// Clear the cart after placing order
	clearCart();

	// Redirect to a thank you or confirmation page
	header('Location: thank-you.php');
	exit();
}


$page = 'order';
include('includes/header.php');

?>

		<div class="p-5 mb-4 jumbotron">
			<div class="container preview-donuts">
				<div class="container-fluid py-5">
					<h1 class="display-5 fw-bold">One more step closer<br>to paradise!</h1>
				</div>
			</div>
		</div>

		<div class="container mb-4">
			<?php if (empty($cart)) { ?>
				<table class="table table-striped">
					<tbody>
						<tr>
							<td class="text-center">Your cart is empty. <a href="eat.php" class="btn btn-success btn-sm">Order some donuts!</a></td>
						</tr>
					</tbody>
				</table>
			<?php } else { ?>
				<table class="table table-striped">
					<thead>
						<tr>
							<th>Donut</th>
							<th>Price</th>
							<th>Quantity</th>
							<th>Subtotal</th>
						</tr>
					</thead>
					<tbody>
						<?php foreach ($cart as $itemId => $quantity): ?>
							<?php foreach ($donuts as $donut): ?>
								<?php if ($donut['id'] == $itemId): ?>
									<tr>
										<td><?php echo $donut['name']; ?></td>
										<td>$<?php echo number_format($donut['price'], 2); ?></td>
										<td><?php echo $quantity; ?></td>
										<td>$<?php echo number_format($donut['price'] * $quantity, 2); ?></td>
									</tr>
								<?php endif; ?>
							<?php endforeach; ?>
						<?php endforeach; ?>
					</tbody>
				</table>

				<div class="text-end">
					<p><strong>Total (before tax):</strong> $<?php echo number_format($total, 2); ?></p>
					<p><strong>Tax (24%):</strong> $<?php echo number_format($tax, 2); ?></p>
					<p><strong>Total (with tax):</strong> $<?php echo number_format($totalWithTax, 2); ?></p>
				</div>

				<div class="row">
					<div class="col-12 col-md-7"></div>
					<div class="col-12 col-md-5">
						<form method="POST" action="order.php">
							<div class="text-end pb-4">
								<div class="input-group mb-3">
									<input type="text" class="form-control" name="name" placeholder="Your name" aria-label="Your name" aria-describedby="place-order-button">
									<button class="btn btn-success" type="submit" id="place-order-button">
										<i class="bi bi-bag-check-fill"></i> Place Order
									</button>
								</div>
							</div>
						</form>
					</div>
				</div>
			<?php } ?>
		</div>

<?php

include('includes/footer.php');
