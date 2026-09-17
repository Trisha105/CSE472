<?php
require "db.php";

$stmt = $pdo->query(
    "SELECT id, full_name, student_id, email, department, workshop, created_at
     FROM registrations
     ORDER BY id DESC"
);
$registrations = $stmt->fetchAll();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Saved Registrations</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <h1>Saved Registrations</h1>
        <p>Registration data retrieved from the MySQL database.</p>
    </header>

    <main>
        <section class="card">
            <?php if (count($registrations) === 0): ?>
                <p>No registration has been saved yet.</p>
            <?php else: ?>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Student ID</th>
                                <th>Email</th>
                                <th>Department</th>
                                <th>Workshop</th>
                                <th>Submitted</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($registrations as $row): ?>
                                <tr>
                                    <td><?php echo htmlspecialchars((string)$row["id"], ENT_QUOTES, 'UTF-8'); ?></td>
                                    <td><?php echo htmlspecialchars($row["full_name"], ENT_QUOTES, 'UTF-8'); ?></td>
                                    <td><?php echo htmlspecialchars($row["student_id"], ENT_QUOTES, 'UTF-8'); ?></td>
                                    <td><?php echo htmlspecialchars($row["email"], ENT_QUOTES, 'UTF-8'); ?></td>
                                    <td><?php echo htmlspecialchars($row["department"], ENT_QUOTES, 'UTF-8'); ?></td>
                                    <td><?php echo htmlspecialchars($row["workshop"], ENT_QUOTES, 'UTF-8'); ?></td>
                                    <td><?php echo htmlspecialchars($row["created_at"], ENT_QUOTES, 'UTF-8'); ?></td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            <?php endif; ?>

            <p><a href="index.php">Back to Registration Form</a></p>
        </section>
    </main>
</body>
</html>
