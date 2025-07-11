<?php
session_start();

class NodeStore
{
    private const SESSION_KEY = 'nervura_nodes';

    public static function setNodes(array $nodes): void
    {
        $_SESSION[self::SESSION_KEY] = $nodes;
    }

    public static function getNodes(): ?array
    {
        return $_SESSION[self::SESSION_KEY] ?? null;
    }

    public static function addNode(array $node): void
    {
        $nodes = self::getNodes() ?? [];
        $nodes[] = $node;
        self::setNodes($nodes);
    }

    public static function updateNode(int $index, array $node): void
    {
        $nodes = self::getNodes() ?? [];
        if (isset($nodes[$index])) {
            $nodes[$index] = $node;
            self::setNodes($nodes);
        }
    }

    public static function removeNode(int $index): void
    {
        $nodes = self::getNodes() ?? [];
        if (isset($nodes[$index])) {
            array_splice($nodes, $index, 1);
            self::setNodes($nodes);
        }
    }

    public static function clear(): void
    {
        unset($_SESSION[self::SESSION_KEY]);
    }
}
