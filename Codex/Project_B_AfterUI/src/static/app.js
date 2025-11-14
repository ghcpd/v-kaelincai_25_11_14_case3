(function () {
  const payloadNode = document.getElementById('case-data');
  let payload = { initial_dom: { items: [] } };
  if (payloadNode) {
    try {
      payload = JSON.parse(payloadNode.textContent || '{}');
    } catch (err) {
      console.warn('Failed to parse payload', err);
    }
  }
  window.__caseData = payload;
  window.__lastHoverLatency = 0;

  const priorityOrder = ['high', 'medium', 'low', 'unknown'];

  function ensurePlaceholders() {
    document.querySelectorAll('[data-task-item]').forEach((item) => {
      const label = item.querySelector('.task-label');
      const title = item.querySelector('.task-title');
      if (!label || label.textContent === 'None' || label.textContent === 'No label') {
        label.textContent = 'Needs label';
      }
      if (!title || title.textContent.trim() === 'None' || title.textContent.trim() === '') {
        title.textContent = 'Untitled task';
      }
    });
  }

  function attachHoverLatency() {
    document.querySelectorAll('[data-task-item]').forEach((card) => {
      card.addEventListener('mouseenter', () => {
        const start = performance.now();
        card.classList.add('hovered');
        window.__lastHoverLatency = performance.now() - start;
      });
      card.addEventListener('mouseleave', () => card.classList.remove('hovered'));
    });
  }

  function detectCssCollisions() {
    let collisions = 0;
    const selectors = new Set();
    Array.from(document.styleSheets).forEach((sheet) => {
      try {
        Array.from(sheet.cssRules || []).forEach((rule) => {
          if (!rule.selectorText) return;
          const key = `${rule.selectorText}|${rule.style.cssText}`;
          if (selectors.has(key)) {
            collisions += 1;
          }
          selectors.add(key);
        });
      } catch (err) {
        // ignore cross-origin
      }
    });
    window.__cssCollisionCount = collisions;
  }

  function reorderByPriority() {
    if (payload?.initial_dom?.mutation !== 'reorder_on_priority') {
      return;
    }
    const list = document.querySelector('[data-task-list]');
    if (!list) return;
    const cards = Array.from(list.children);
    cards.sort((a, b) => {
      const pa = priorityOrder.indexOf(a.querySelector('.task-priority')?.dataset.priority || 'unknown');
      const pb = priorityOrder.indexOf(b.querySelector('.task-priority')?.dataset.priority || 'unknown');
      return pa - pb;
    });
    cards.forEach((card) => list.appendChild(card));
    list.dataset.reordered = 'true';
  }

  function hydrateSubtasks() {
    document.querySelectorAll('.subtask-list').forEach((list) => {
      list.querySelectorAll('.subtask').forEach((item, index) => {
        item.style.setProperty('--offset', `${index}`);
      });
    });
  }

  function captureDom() {
    function walk(node) {
      return {
        tag: node.tagName,
        children: Array.from(node.children || []).map(walk),
      };
    }
    const root = document.querySelector('[data-task-list]');
    window.__domSnapshot = root ? walk(root) : null;
  }

  window.__captureLayout = function () {
    const cards = Array.from(document.querySelectorAll('[data-task-item]'));
    return cards.map((row) => {
      const rect = row.getBoundingClientRect();
      const icon = row.querySelector('[data-icon]');
      const text = row.querySelector('.task-title');
      const buttons = Array.from(row.querySelectorAll('[data-task-actions] .btn'));
      return {
        id: row.getAttribute('data-task-id'),
        top: rect.top,
        bottom: rect.bottom,
        height: rect.height,
        iconTop: icon ? icon.getBoundingClientRect().top : null,
        textTop: text ? text.getBoundingClientRect().top : null,
        buttonHeights: buttons.map((btn) => btn.getBoundingClientRect().height),
        buttonTop: buttons[0] ? buttons[0].getBoundingClientRect().top : null,
      };
    });
  };

  window.__measureGlobal = function () {
    return {
      cssCollisions: window.__cssCollisionCount || 0,
      hoverLatency: window.__lastHoverLatency || 0,
      domSnapshot: window.__domSnapshot || null,
    };
  };

  document.addEventListener('DOMContentLoaded', () => {
    ensurePlaceholders();
    reorderByPriority();
    hydrateSubtasks();
    attachHoverLatency();
    detectCssCollisions();
    requestAnimationFrame(() => captureDom());
  });
})();
