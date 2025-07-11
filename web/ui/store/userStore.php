<?php
session_start();

class UserStore
{
    private const SESSION_KEY = 'nervura_user';

    // Sauvegarder les données utilisateur en session
    public static function setUser(array $userData): void
    {
        $_SESSION[self::SESSION_KEY] = $userData;
    }

    // Récupérer les données utilisateur depuis la session
    public static function getUser(): ?array
    {
        return $_SESSION[self::SESSION_KEY] ?? null;
    }

    // Vérifier si un utilisateur est connecté
    public static function isLoggedIn(): bool
    {
        return isset($_SESSION[self::SESSION_KEY]);
    }

    // Déconnecter l'utilisateur et nettoyer la session
    public static function logout(): void
    {
        unset($_SESSION[self::SESSION_KEY]);
        session_regenerate_id(true);
    }

    // Mettre à jour un champ spécifique de l'utilisateur en session
    public static function updateField(string $field, $value): void
    {
        if (self::isLoggedIn()) {
            $_SESSION[self::SESSION_KEY][$field] = $value;
        }
    }

    // Retourne l'ID de l'utilisateur connecté ou null
    public static function getUserId(): ?int
    {
        $user = self::getUser();
        return $user['id'] ?? null;
    }

    // Retourne le rôle ou les permissions de l'utilisateur
    public static function getUserRole(): ?string
    {
        $user = self::getUser();
        return $user['role'] ?? null;
    }

    // Vérifier si l'utilisateur a un rôle admin
    public static function isAdmin(): bool
    {
        return self::getUserRole() === 'admin';
    }

    // Stocker un token CSRF ou API spécifique à l'utilisateur
    public static function setToken(string $token): void
    {
        if (self::isLoggedIn()) {
            $_SESSION[self::SESSION_KEY]['token'] = $token;
        }
    }

    // Récupérer le token utilisateur stocké
    public static function getToken(): ?string
    {
        $user = self::getUser();
        return $user['token'] ?? null;
    }
}
