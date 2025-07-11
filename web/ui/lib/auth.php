<?php
// lib/auth.php
// Gestion de l'authentification utilisateur, sessions, tokens

session_start();

function isLoggedIn(): bool {
    return isset($_SESSION['user_id']);
}

function getUserId(): ?int {
    return $_SESSION['user_id'] ?? null;
}

function loginUser(int $userId, string $username, string $token): void {
    $_SESSION['user_id'] = $userId;
    $_SESSION['username'] = $username;
    $_SESSION['token'] = $token;
}

function logoutUser(): void {
    session_unset();
    session_destroy();
}

function getAuthToken(): ?string {
    return $_SESSION['token'] ?? null;
}

function requireLogin(): void {
    if (!isLoggedIn()) {
        header("Location: /ui/pages/login.php");
        exit;
    }
}
