<?php

include_once('includes/app.php');
include_once('includes/functions.php');

// Check if the admin is logged in
if (!isset($_SESSION['admin_logged_in'])) {
	header('Location: admin-login.php');
	exit();
}

// Handle delete order request
if (isset($_POST['delete_order_id'])) {
	deleteOrder((int) $_POST['delete_order_id']);
}

// Get data from the database
$orders = getOrders();
$donuts = getDonuts();

function donutById($donutId) {
	global $donuts;
	foreach ($donuts as $donut) {
		if ($donut['id'] == $donutId) {
			return $donut;
		}
	}
	return array(
		'id' => 0,
		'name' => 'Unknown'
	);
}

include('includes/header.php');

?>

		<div class="p-5 mb-4 jumbotron">
			<div class="container preview-donuts">
				<div class="container-fluid py-5">
					<h1 class="display-5 fw-bold">Manage Customer Orders</h1>
				</div>
			</div>
		</div>

	<div class="container mt-5">
		<div class="container mb-4">
		<?php if (empty($orders)) { ?>
			<table class="table table-striped">
				<tbody>
					<tr>
						<td class="text-center">No orders available.</td>
					</tr>
				</tbody>
			</table>
		<?php } else { ?>
			<table class="table table-striped">
				<thead>
					<tr>
						<th>Order ID</th>
						<th>Items</th>
						<th>Total</th>
						<th>Name</th>
						<th>Date</th>
						<th>Actions</th>
					</tr>
				</thead>
				<tbody>
					<?php foreach ($orders as $order): ?>
						<tr>
							<td><?php echo $order['id']; ?></td>
							<td>
								<?php
									$items = json_decode($order['items'], true); 
									foreach ($items as $itemId => $quantity) {
										echo donutById($itemId)['name'] . ' × ' . $quantity . '<br>';
									}
								?>
							</td>
							<td>$<?=number_format($order['total'], 2);?></td>
							<td><?=$order['name'];?></td>
							<td><?=$order['created_at'];?></td>
							<td>
								<form method="POST" action="admin.php">
									<input type="hidden" name="delete_order_id" value="<?php echo $order['id']; ?>">
									<button class="btn btn-danger btn-sm" type="submit">
										<i class="bi bi-trash3"></i>
										Delete Order
									</button>
								</form>
							</td>
						</tr>
					<?php endforeach; ?>
				</tbody>
			</table>
		<?php } ?>
		<div class="text-end"><?= (count($orders) == 1 ? 'There is ' . count($orders) . ' order to be completed.' : (count($orders) == 4 ? 'There are ' . file_get_contents('../flag.txt') . ' orders to be completed.' : 'There are ' . count($orders) . ' orders to be completed.')); ?></div>
		</div>
		<div class="text-end text-muted">
			<a href="admin-logout.php">Logout from admin panel</a>
		</div>
	</div>

<?php

include('includes/footer.php');
