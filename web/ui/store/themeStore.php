<?php
session_start();

class ThemeStore
{
    private const SESSION_KEY = 'nervura_theme';

    public static function setThemes(array $themes): void
    {
        $_SESSION[self::SESSION_KEY] = $themes;
    }

    public static function getThemes(): ?array
    {
        return $_SESSION[self::SESSION_KEY] ?? null;
    }

    public static function addTheme(array $theme): void
    {
        $themes = self::getThemes() ?? [];
        $themes[] = $theme;
        self::setThemes($themes);
    }

    public static function updateTheme(int $index, array $theme): void
    {
        $themes = self::getThemes() ?? [];
        if (isset($themes[$index])) {
            $themes[$index] = $theme;
            self::setThemes($themes);
        }
    }

    public static function removeTheme(int $index): void
    {
        $themes = self::getThemes() ?? [];
        if (isset($themes[$index])) {
            array_splice($themes, $index, 1);
            self::setThemes($themes);
        }
    }

    public static function clear(): void
    {
        unset($_SESSION[self::SESSION_KEY]);
    }
}
