<?php
session_start();

require_once __DIR__ . '/../store/systemStore.php';
require_once __DIR__ . '/../store/nodeStore.php';
require_once __DIR__ . '/../store/themeStore.php';
require_once __DIR__ . '/../store/vmStore.php';
require_once __DIR__ . '/../store/pluginStore.php';
require_once __DIR__ . '/../store/appStore.php';

header('Content-Type: application/json');

$action = $_POST['action'] ?? null;
$store = $_POST['store'] ?? null;
$data = $_POST['data'] ?? null;
$index = isset($_POST['index']) ? intval($_POST['index']) : null;

if (!$action || !$store) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing parameters']);
    exit;
}

switch ($store) {
    case 'system':
        handleStore(SystemStore::class, $action, $data, $index);
        break;
    case 'node':
        handleStore(NodeStore::class, $action, $data, $index);
        break;
    case 'theme':
        handleStore(ThemeStore::class, $action, $data, $index);
        break;
    case 'vm':
        handleStore(VmStore::class, $action, $data, $index);
        break;
    case 'plugin':
        handleStore(PluginStore::class, $action, $data, $index);
        break;
    case 'app':
        handleStore(AppStore::class, $action, $data, $index);
        break;
    default:
        http_response_code(400);
        echo json_encode(['error' => 'Unknown store']);
        exit;
}

function handleStore(string $class, string $action, $data, ?int $index): void
{
    switch ($action) {
        case 'get':
            $result = $class::{"get" . ucfirst(rtrim(basename(strtolower($class)), 'Store'))}();
            echo json_encode(['success' => true, 'data' => $result]);
            break;

        case 'set':
            if (!is_array($data)) {
                http_response_code(400);
                echo json_encode(['error' => 'Invalid data']);
                return;
            }
            $class::{"set" . ucfirst(rtrim(basename(strtolower($class)), 'Store')}($data);
            echo json_encode(['success' => true]);
            break;

        case 'add':
            if (!is_array($data)) {
                http_response_code(400);
                echo json_encode(['error' => 'Invalid data']);
                return;
            }
            $class::{"add" . ucfirst(rtrim(basename(strtolower($class)), 'Store')}($data);
            echo json_encode(['success' => true]);
            break;

        case 'update':
            if ($index === null || !is_array($data)) {
                http_response_code(400);
                echo json_encode(['error' => 'Missing index or invalid data']);
                return;
            }
            $class::{"update" . ucfirst(rtrim(basename(strtolower($class)), 'Store')}($index, $data);
            echo json_encode(['success' => true]);
            break;

        case 'remove':
            if ($index === null) {
                http_response_code(400);
                echo json_encode(['error' => 'Missing index']);
                return;
            }
            $class::{"remove" . ucfirst(rtrim(basename(strtolower($class)), 'Store')}($index);
            echo json_encode(['success' => true]);
            break;

        case 'clear':
            $class::clear();
            echo json_encode(['success' => true]);
            break;

        default:
            http_response_code(400);
            echo json_encode(['error' => 'Unknown action']);
    }
}
