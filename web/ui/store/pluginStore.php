<?php
session_start();

class PluginStore
{
    private const SESSION_KEY = 'nervura_plugins';

    public static function setPlugins(array $plugins): void
    {
        $_SESSION[self::SESSION_KEY] = $plugins;
    }

    public static function getPlugins(): ?array
    {
        return $_SESSION[self::SESSION_KEY] ?? null;
    }

    public static function addPlugin(array $plugin): void
    {
        $plugins = self::getPlugins() ?? [];
        $plugins[] = $plugin;
        self::setPlugins($plugins);
    }

    public static function updatePlugin(int $index, array $plugin): void
    {
        $plugins = self::getPlugins() ?? [];
        if (isset($plugins[$index])) {
            $plugins[$index] = $plugin;
            self::setPlugins($plugins);
        }
    }

    public static function removePlugin(int $index): void
    {
        $plugins = self::getPlugins() ?? [];
        if (isset($plugins[$index])) {
            array_splice($plugins, $index, 1);
            self::setPlugins($plugins);
        }
    }

    public static function clear(): void
    {
        unset($_SESSION[self::SESSION_KEY]);
    }
}
