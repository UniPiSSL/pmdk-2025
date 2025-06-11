<?php

require_once('includes/app.php');

$page = 'home';
include('includes/header.php');

?>

		<div class="p-5 mb-4 jumbotron">
			<div class="container preview-donuts">
				<div class="container-fluid py-5">
					<h1 class="display-5 fw-bold">Pick donuts<br>your way!</h1>
					<p class="col-md-8 fs-4">Pick the donuts you like, the way you like and have them ready for pick up in 10 minutes.</p>
					<a  href="eat.php" class="btn btn-danger btn-lg">Order Now!</a>
				</div>
			</div>
		</div>

<?php

include('includes/footer.php');
