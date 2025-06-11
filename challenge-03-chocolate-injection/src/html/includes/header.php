<?php

include_once('includes/app.php');
include_once('includes/functions.php');

$items_in_cart = count(getCart());

?>
<!doctype html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title><?=WEBSITE_TITLE;?></title>
		<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
		<link href="css/bootstrap.css" rel="stylesheet">
		<link href="css/style.css" rel="stylesheet">
	</head>
	<body>
		<nav class="navbar navbar-expand-lg bg-dark" data-bs-theme="dark">
			<div class="container">
				<a class="navbar-brand" href="/"><?=WEBSITE_BRAND_NAME;?></a>
				<div class="collapse navbar-collapse" id="navbarColor02">
					<div class="me-auto text-muted fst-italic"><small><?=WEBSITE_BRAND_TAGLINE;?></small></div>
					<div class="d-flex">
						<ul class="navbar-nav">
							<li class="nav-item">
								<a class="nav-link active" href="order.php">
									<?php if ($items_in_cart > 0) { ?><span class="badge text-bg-secondary"><?=$items_in_cart;?></span><?php } ?>
									<i class="bi bi-cart2"></i>
								</a>
							</li>
						</ul>
					</div>
				</div>
			</div>
		</nav>

		<nav class="navbar navbar-expand-lg bg-body-tertiary">
			<div class="container">
				<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
				<span class="navbar-toggler-icon"></span>
				</button>
				<div class="collapse navbar-collapse" id="navbarNav">
					<ul class="navbar-nav">
						<li class="nav-item">
							<a class="nav-link<?=(isset($page) && $page == 'home'?' active':'');?>" aria-current="page" href="index.php">Home</a>
						</li>
						<li class="nav-item">
							<a class="nav-link<?=(isset($page) && $page == 'eat'?' active':'');?>" href="eat.php">Order</a>
						</li>
					</ul>
				</div>
			</div>
		</nav>
