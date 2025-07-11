<?php
class Translate {
    private $translations = [];
    private $lang;

    public function __construct(string $lang = "en") {
        $this->lang = $lang;
        $path = __DIR__ . "/../../i18n/{$lang}.json";
        if (!file_exists($path)) {
            $path = __DIR__ . "/../../i18n/en.json";
        }
        $json = file_get_contents($path);
        $this->translations = json_decode($json, true);
    }

    public function get(string $key): string {
        return $this->translations[$key] ?? $key;
    }
}
