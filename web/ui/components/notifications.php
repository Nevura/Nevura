<?php
include_once __DIR__ . '/../lib/api.php';
include_once __DIR__ . '/../lib/utils.php';
include_once __DIR__ . '/../store/userStore.php';

$notifications = getNotifications();
$unreadCount = count(array_filter($notifications, fn($n) => !$n['read']));

// Mappage simple pour icônes Lucide (nom icone par défaut 'info')
function getLucideIconName($type) {
    $map = [
        'error' => 'alert-circle',
        'warning' => 'alert-triangle',
        'success' => 'check-circle',
        'info' => 'info',
        'mail' => 'mail',
        'system' => 'cpu',
        'security' => 'shield-check',
    ];
    return $map[$type] ?? 'info';
}
?>

<!-- Icône Notification -->
<div id="notif-icon-wrapper" class="fixed top-4 right-4 z-50">
  <button onclick="toggleNotificationPanel()" class="relative" aria-label="Notifications">
    <svg class="w-7 h-7 stroke-zinc-700 dark:stroke-zinc-200" xmlns="http://www.w3.org/2000/svg" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
    </svg>
    <span id="notif-count" class="absolute -top-1 -right-1 bg-red-600 text-white text-xs font-bold px-1.5 py-0.5 rounded-full min-w-[20px] text-center <?= $unreadCount > 0 ? '' : 'hidden' ?>">
      <?= $unreadCount > 99 ? '99+' : $unreadCount ?>
    </span>
  </button>
</div>

<!-- Overlay -->
<div id="notif-overlay" class="fixed inset-0 bg-black bg-opacity-40 z-40 hidden" onclick="closeNotificationPanel()"></div>

<!-- Panneau Notifications -->
<div id="notif-panel" class="fixed top-0 right-0 h-full w-[340px] max-w-full bg-white dark:bg-zinc-900 shadow-lg z-50 transform translate-x-full transition-transform duration-300 ease-in-out overflow-y-auto" role="region" aria-label="Liste des notifications">
  <div class="p-4 border-b border-zinc-200 dark:border-zinc-800 flex justify-between items-center">
    <h3 class="text-lg font-semibold">Notifications</h3>
    <button onclick="clearAllNotifications()" class="text-sm text-red-500 hover:underline" aria-label="Supprimer toutes les notifications">Tout supprimer</button>
  </div>

  <div id="notif-list" class="divide-y divide-zinc-200 dark:divide-zinc-800" role="list">
    <?php foreach ($notifications as $notif): 
      $iconName = getLucideIconName($notif['type'] ?? 'info');
    ?>
      <div class="p-4 flex items-start gap-3 notif-entry <?= $notif['read'] ? '' : 'bg-zinc-100 dark:bg-zinc-800' ?>" role="listitem" tabindex="0" aria-live="polite" aria-atomic="true">
        <div class="w-6 h-6 text-zinc-600 dark:text-zinc-300" data-icon="<?= $iconName ?>"></div>
        <div class="flex-1">
          <p class="text-sm font-medium truncate" title="<?= htmlentities($notif['title']) ?>"><?= htmlentities($notif['title']) ?></p>
          <p class="text-xs text-zinc-600 dark:text-zinc-400 truncate" title="<?= htmlentities($notif['message']) ?>"><?= htmlentities($notif['message']) ?></p>
        </div>
        <button onclick="removeNotification(<?= $notif['id'] ?>)" class="text-zinc-400 hover:text-red-500" aria-label="Supprimer cette notification">&times;</button>
      </div>
    <?php endforeach; ?>
  </div>
</div>

<!-- Script Lucide + gestion notifications -->
<script src="https://cdn.jsdelivr.net/npm/lucide@latest/dist/lucide.min.js"></script>
<script>
  // Init lucide icons in notif panel dynamically
  function renderLucideIcons() {
    document.querySelectorAll('[data-icon]').forEach(el => {
      const iconName = el.getAttribute('data-icon');
      el.innerHTML = lucide.icons[iconName].toSvg({width: 24, height: 24, strokeWidth: 2, stroke: 'currentColor'});
    });
  }

  let notifOpen = false;

  function toggleNotificationPanel() {
    notifOpen ? closeNotificationPanel() : openNotificationPanel();
  }

  function openNotificationPanel() {
    document.getElementById("notif-panel").classList.remove("translate-x-full");
    document.getElementById("notif-overlay").classList.remove("hidden");
    notifOpen = true;
    markAllAsRead();
    updateNotifCount(0);
  }

  function closeNotificationPanel() {
    document.getElementById("notif-panel").classList.add("translate-x-full");
    document.getElementById("notif-overlay").classList.add("hidden");
    notifOpen = false;
  }

  function markAllAsRead() {
    fetch('/api/alerts/read-all', { method: 'POST' });
    const entries = document.querySelectorAll('.notif-entry');
    entries.forEach(el => el.classList.remove("bg-zinc-100", "dark:bg-zinc-800"));
  }

  function updateNotifCount(count) {
    const badge = document.getElementById("notif-count");
    if (count > 0) {
      badge.textContent = count > 99 ? "99+" : count;
      badge.classList.remove("hidden");
    } else {
      badge.classList.add("hidden");
    }
  }

  function removeNotification(id) {
    fetch(`/api/alerts/${id}`, { method: 'DELETE' }).then(() => {
      const el = document.querySelector(`.notif-entry[onclick*="removeNotification(${id})"]`);
      if (el) el.remove();
    });
  }

  function clearAllNotifications() {
    fetch('/api/alerts/clear', { method: 'POST' }).then(() => {
      document.getElementById("notif-list").innerHTML = '';
      updateNotifCount(0);
      closeNotificationPanel();
    });
  }

  // Call lucide render after DOM loaded
  document.addEventListener("DOMContentLoaded", () => {
    renderLucideIcons();
  });
</script>
