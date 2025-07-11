<?php
session_start();

class AppStore
{
    private const SESSION_KEY = 'nervura_apps';

    public static function setApps(array $apps): void
    {
        $_SESSION[self::SESSION_KEY] = $apps;
    }

    public static function getApps(): ?array
    {
        return $_SESSION[self::SESSION_KEY] ?? null;
    }

    public static function addApp(array $app): void
    {
        $apps = self::getApps() ?? [];
        $apps[] = $app;
        self::setApps($apps);
    }

    public static function updateApp(int $index, array $app): void
    {
        $apps = self::getApps() ?? [];
        if (isset($apps[$index])) {
            $apps[$index] = $app;
            self::setApps($apps);
        }
    }

    public static function removeApp(int $index): void
    {
        $apps = self::getApps() ?? [];
        if (isset($apps[$index])) {
            array_splice($apps, $index, 1);
            self::setApps($apps);
        }
    }

    public static function clear(): void
    {
        unset($_SESSION[self::SESSION_KEY]);
    }
}
