<?php
session_start();

class VmStore
{
    private const SESSION_KEY = 'nervura_vms';

    public static function setVms(array $vms): void
    {
        $_SESSION[self::SESSION_KEY] = $vms;
    }

    public static function getVms(): ?array
    {
        return $_SESSION[self::SESSION_KEY] ?? null;
    }

    public static function addVm(array $vm): void
    {
        $vms = self::getVms() ?? [];
        $vms[] = $vm;
        self::setVms($vms);
    }

    public static function updateVm(int $index, array $vm): void
    {
        $vms = self::getVms() ?? [];
        if (isset($vms[$index])) {
            $vms[$index] = $vm;
            self::setVms($vms);
        }
    }

    public static function removeVm(int $index): void
    {
        $vms = self::getVms() ?? [];
        if (isset($vms[$index])) {
            array_splice($vms, $index, 1);
            self::setVms($vms);
        }
    }

    public static function clear(): void
    {
        unset($_SESSION[self::SESSION_KEY]);
    }
}
