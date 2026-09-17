<?php
$pageTitle = "Workshop Registration";
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $pageTitle; ?></title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <h1>Student Workshop Registration System</h1>
        <p>Register for a practical web development workshop.</p>
    </header>

    <main>
        <section class="card">
            <h2>Registration Form</h2>

            <form action="save_registration.php" method="POST">
                <label for="fullName">Full Name</label>
                <input type="text" id="fullName" name="full_name" required>

                <label for="studentId">Student ID</label>
                <input type="text" id="studentId" name="student_id" required>

                <label for="email">Email Address</label>
                <input type="email" id="email" name="email" required>

                <label for="department">Department</label>
                <select id="department" name="department" required>
                    <option value="">Select Department</option>
                    <option value="CSE">CSE</option>
                    <option value="EEE">EEE</option>
                    <option value="Textile Engineering">Textile Engineering</option>
                    <option value="English">English</option>
                    <option value="BBA">BBA</option>
                </select>

                <label for="workshop">Workshop</label>
                <select id="workshop" name="workshop" required>
                    <option value="">Select Workshop</option>
                    <option value="HTML and CSS Foundations">HTML and CSS Foundations</option>
                    <option value="JavaScript Basics">JavaScript Basics</option>
                    <option value="PHP and MySQL Basics">PHP and MySQL Basics</option>
                    <option value="Database Foundations">Database Foundations</option>
                </select>

                <label for="expectation">What do you expect to learn?</label>
                <textarea id="expectation" name="expectation" rows="4"></textarea>

                <button type="submit">Submit Registration</button>
            </form>
        </section>

        <p class="link-row"><a href="registrations.php">View Saved Registrations</a></p>
    </main>
</body>
</html>
