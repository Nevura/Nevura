<?php
// lib/api.php
// Fonctions pour effectuer des requêtes AJAX/fetch vers l'API backend (FastAPI)

function apiRequest(string $method, string $endpoint, array $data = null, string $token = null): array {
    $url = "/api" . $endpoint;
    $headers = [
        "Accept: application/json",
        "Content-Type: application/json"
    ];
    if ($token !== null) {
        $headers[] = "Authorization: Bearer " . $token;
    }

    $options = [
        "http" => [
            "method" => strtoupper($method),
            "header" => implode("\r\n", $headers),
            "ignore_errors" => true,
        ]
    ];

    if ($data !== null) {
        $options["http"]["content"] = json_encode($data);
    }

    $context = stream_context_create($options);
    $result = @file_get_contents($url, false, $context);

    if ($result === false) {
        return ["error" => "API request failed"];
    }

    $response = json_decode($result, true);

    if ($response === null) {
        return ["error" => "Invalid JSON response"];
    }

    return $response;
}

function apiGet(string $endpoint, string $token = null): array {
    return apiRequest("GET", $endpoint, null, $token);
}

function apiPost(string $endpoint, array $data, string $token = null): array {
    return apiRequest("POST", $endpoint, $data, $token);
}

function apiPut(string $endpoint, array $data, string $token = null): array {
    return apiRequest("PUT", $endpoint, $data, $token);
}

function apiDelete(string $endpoint, string $token = null): array {
    return apiRequest("DELETE", $endpoint, null, $token);
}
async function storeAction(store, action, data = null, index = null) {
  const formData = new FormData();
  formData.append('store', store);
  formData.append('action', action);
  if (data) formData.append('data', JSON.stringify(data));
  if (index !== null) formData.append('index', index);

  const response = await fetch('/web/ui/lib/ajaxHandlers.php', {
    method: 'POST',
    body: formData,
  });
  return response.json();
}
