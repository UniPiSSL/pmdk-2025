<?php

include_once('includes/app.php');
include_once('includes/functions.php');

$error = '';

// Handle login form submission
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
	$username = $_POST['username'];
	$password = $_POST['password'];

	if (verifyCredentials($username, $password)) {
		$_SESSION['admin_logged_in'] = true;
		header('Location: admin.php');
		exit();
	} else {
		$error = 'Invalid username or password';
	}
}

include('includes/header.php');

?>
		<div class="p-5 mb-4 jumbotron">
			<div class="container pb-4">
				<div class="row">
					<div class="col-12 col-md-8"></div>
					<div class="col-12 col-md-4">
						<h1 class="text-center">Admin Login</h1>
						<?php if ($error): ?>
							<div class="alert alert-danger text-center"><?php echo $error; ?></div>
						<?php endif; ?>

						<form method="POST" action="admin-login.php" autocomplete="off">
							<div class="mb-3">
								<label for="username" class="form-label">Username</label>
								<input type="text" name="username" class="form-control" required>
							</div>
							<div class="mb-3">
								<label for="password" class="form-label">Password</label>
								<input type="password" name="password" class="form-control" required>
							</div>
							<div class="text-center">
								<button class="btn btn-primary w-100" type="submit">Login</button>
							</div>
						</form>
					</div>
				</div>
			</div>
		</div>
		

<?php

include('includes/footer.php');
