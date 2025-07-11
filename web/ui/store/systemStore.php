<?php
session_start();

class SystemStore
{
    private const SESSION_KEY = 'nervura_system';

    public static function setSettings(array $settings): void
    {
        $_SESSION[self::SESSION_KEY] = $settings;
    }

    public static function getSettings(): ?array
    {
        return $_SESSION[self::SESSION_KEY] ?? null;
    }

    public static function updateSetting(string $key, $value): void
    {
        if (isset($_SESSION[self::SESSION_KEY])) {
            $_SESSION[self::SESSION_KEY][$key] = $value;
        }
    }

    public static function clear(): void
    {
        unset($_SESSION[self::SESSION_KEY]);
    }
}
