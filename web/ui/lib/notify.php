<?php
// lib/notify.php
// Gestion des notifications utilisateur

require_once __DIR__ . '/../db/connection.php'; // Connexion à la DB

function getNotifications(int $userId): array {
    $pdo = getDbConnection();
    $stmt = $pdo->prepare("SELECT id, message, type, created_at, read_at FROM notifications WHERE user_id = :user_id ORDER BY created_at DESC LIMIT 100");
    $stmt->execute(['user_id' => $userId]);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

function markNotificationsRead(int $userId): bool {
    $pdo = getDbConnection();
    $stmt = $pdo->prepare("UPDATE notifications SET read_at = NOW() WHERE user_id = :user_id AND read_at IS NULL");
    return $stmt->execute(['user_id' => $userId]);
}

function deleteNotification(int $notificationId, int $userId): bool {
    $pdo = getDbConnection();
    $stmt = $pdo->prepare("DELETE FROM notifications WHERE id = :id AND user_id = :user_id");
    return $stmt->execute(['id' => $notificationId, 'user_id' => $userId]);
}

function clearNotifications(int $userId): bool {
    $pdo = getDbConnection();
    $stmt = $pdo->prepare("DELETE FROM notifications WHERE user_id = :user_id");
    return $stmt->execute(['user_id' => $userId]);
}

function createNotification(int $userId, string $message, string $type = "info"): bool {
    $pdo = getDbConnection();
    $stmt = $pdo->prepare("INSERT INTO notifications (user_id, message, type, created_at) VALUES (:user_id, :message, :type, NOW())");
    return $stmt->execute(['user_id' => $userId, 'message' => $message, 'type' => $type]);
}

function getIconForType(string $type): string {
    // Simple mapping SVG strings for icons (could be replaced by lucide icons)
    switch ($type) {
        case 'info': return '<svg class="icon info" ...></svg>';
        case 'warning': return '<svg class="icon warning" ...></svg>';
        case 'error': return '<svg class="icon error" ...></svg>';
        default: return '<svg class="icon default" ...></svg>';
    }
}
