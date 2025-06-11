<?php

include_once('includes/app.php');
include_once('includes/functions.php');

// Handle search query
$searchQuery = isset($_GET['search']) ? $_GET['search'] : '';

// Fetch donuts from the database
$donuts = getDonuts($searchQuery);
$cart = getCart();

$page = 'eat';
include('includes/header.php');

?>

		<div class="p-5 mb-4 jumbotron">
			<div class="container preview-donuts">
				<div class="container-fluid py-5">
					<h1 class="display-5 fw-bold">Choose Your<br>Donuts!</h1>
				</div>
			</div>
		</div>

		<div class="container mt-5">

			<!-- Search form -->
			<form method="GET" action="eat.php" class="mb-4" autocomplete="off">
				<div class="input-group">
					<input type="text" name="search" class="form-control" placeholder="Search for donuts" value="<?php echo htmlspecialchars($searchQuery); ?>">
					<button class="btn btn-primary" type="submit">
						<i class="bi bi-search"></i> Search
					</button>
				</div>
			</form>

			<!-- Display donuts -->
			<div class="row">
				<?php if (empty($donuts)): ?>
					<p class="text-center">No donuts found.</p>
				<?php else: ?>
					<?php foreach ($donuts as $donut): ?>
						<div class="col-6 col-md-4 col-lg-3 mb-4">
							<div class="card">
								<img src="<?php echo $donut['image']; ?>" class="card-img-top" alt="<?php echo $donut['name']; ?>">
								<div class="card-body">
									<h5 class="card-title"><?php echo $donut['name']; ?></h5>
									<p class="card-text">Price: $<?php echo number_format($donut['price'], 2); ?></p>
									<form method="POST" action="add-to-cart.php">
										<input type="hidden" name="id" value="<?php echo $donut['id']; ?>">
										<div class="input-group">
											<?php if (isset($cart[$donut['id']])) { ?>
												<input type="number" name="quantity" class="form-control" value="<?=$cart[$donut['id']];?>" min="0">
												<button class="btn btn-info" type="submit" title="Update Cart">
													<i class="bi bi-arrow-clockwise"></i>
												</button>
											<?php } else { ?>
												<input type="number" name="quantity" class="form-control" value="1" min="0">
												<button class="btn btn-success" type="submit" title="Add to Cart">
													<i class="bi bi-plus"></i>
												</button>
											<?php } ?>
										</div>
									</form>
								</div>
							</div>
						</div>
					<?php endforeach; ?>
				<?php endif; ?>
			</div>
		</div>
		<?php if (count($cart) > 0) { ?>
		<div class="container mb-4 text-end">
			<a href="order.php" class="btn btn-success">
				<i class="bi bi-card-checklist"></i> View and Submit your order!
			</a>
		</div>
		<?php } ?>

<?php

include('includes/footer.php');
