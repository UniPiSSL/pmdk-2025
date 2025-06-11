<?php

// Disable errors
//error_reporting(0);
//ini_set('display_errors', 0);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);


define("WEBSITE_TITLE", "ChocolateInjection");
define("WEBSITE_DESCRIPTION", "Your go-to place for delicious, fresh doughnuts with a rich chocolate twist.");
define("WEBSITE_BRAND_NAME", "ChocolateInjection");
define("WEBSITE_BRAND_TAGLINE", "Just donuts");
define("WEBSITE_BRAND_ADDRESS", "123 Doughnut Lane, Sweet City");
define("WEBSITE_BRAND_TELEPHONE", "+30 234 567 890, +30 234 567 891");
define("WEBSITE_BRAND_EMAIL", "info@chocolateinjection.com");
define("WEBSITE_COPYRIGHT", "© " . date("Y") . " Chocolate Injection. All Rights Reserved.");
define("WEBSITE_DATABASE_PATH", realpath(__DIR__ . "/../../db") . '/database.db');

// Load Database
require_once(__DIR__ . '/database.php');

// Start session
session_start();
