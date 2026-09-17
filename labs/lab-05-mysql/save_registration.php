<?php
require "db.php";

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    header("Location: index.php");
    exit;
}

$fullName = trim($_POST["full_name"] ?? "");
$studentId = trim($_POST["student_id"] ?? "");
$email = trim($_POST["email"] ?? "");
$department = trim($_POST["department"] ?? "");
$workshop = trim($_POST["workshop"] ?? "");
$expectation = trim($_POST["expectation"] ?? "");

if ($fullName === "" || $studentId === "" || $email === "" || $department === "" || $workshop === "") {
    die("Please complete all required fields.");
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    die("Please enter a valid email address.");
}

$sql = "INSERT INTO registrations
        (full_name, student_id, email, department, workshop, expectation)
        VALUES
        (:full_name, :student_id, :email, :department, :workshop, :expectation)";

$stmt = $pdo->prepare($sql);
$stmt->execute([
    ":full_name" => $fullName,
    ":student_id" => $studentId,
    ":email" => $email,
    ":department" => $department,
    ":workshop" => $workshop,
    ":expectation" => $expectation
]);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration Saved</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <main>
        <section class="card status-card">
            <h1>Registration Saved</h1>
            <p>Thank you, <?php echo htmlspecialchars($fullName, ENT_QUOTES, 'UTF-8'); ?>. Your registration has been saved successfully.</p>
            <p><a href="registrations.php">View Saved Registrations</a></p>
            <p><a href="index.php">Submit Another Registration</a></p>
        </section>
    </main>
</body>
</html>
