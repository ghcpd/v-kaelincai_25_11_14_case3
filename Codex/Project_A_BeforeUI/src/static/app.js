(function () {
  const payloadNode = document.getElementById('case-data');
  let payload = { initial_dom: { items: [] } };
  if (payloadNode) {
    try {
      payload = JSON.parse(payloadNode.textContent || '{}');
    } catch (err) {
      console.error('payload parse error', err);
    }
  }
  window.__caseData = payload;
  window.__lastHoverLatency = 120;

  function attachHoverLatency() {
    document.querySelectorAll('[data-task-item]').forEach((item, index) => {
      item.addEventListener('mouseenter', () => {
        const start = performance.now();
        setTimeout(() => {
          item.classList.add('hovered');
          window.__lastHoverLatency = performance.now() - start;
        }, 48 + index * 4);
      });
    });
  }

  function detectCssCollisions() {
    let collisions = 0;
    const selectors = new Set();
    try {
      Array.from(document.styleSheets).forEach((sheet) => {
        Array.from(sheet.cssRules || []).forEach((rule) => {
          if (!rule.selectorText) return;
          if (selectors.has(rule.selectorText)) {
            collisions += 1;
          }
          selectors.add(rule.selectorText);
        });
      });
    } catch (err) {
      collisions = 4; // pessimistic default when parsing fails
    }
    window.__cssCollisionCount = collisions;
  }

  function applyMutation() {
    const mutation = payload?.initial_dom?.mutation;
    if (mutation === 'reorder_on_priority') {
      const list = document.querySelector('[data-task-list]');
      if (!list) return;
      const items = Array.from(list.children);
      if (items.length > 1) {
        list.appendChild(items[0]);
      }
      list.dataset.reordered = 'true';
    }
  }

  function renderNestedSubtasks() {
    document.querySelectorAll('[data-subtasks]').forEach((wrapper) => {
      wrapper.setAttribute('role', 'group');
      wrapper.querySelectorAll('.subtask').forEach((sub, idx) => {
        sub.setAttribute('data-depth', idx);
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
    const rows = Array.from(document.querySelectorAll('[data-task-item]'));
    return rows.map((row) => {
      const rect = row.getBoundingClientRect();
      const icon = row.querySelector('[data-icon]');
      const text = row.querySelector('.task-title');
      const buttons = Array.from(row.querySelectorAll('.task-actions button'));
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
      hoverLatency: window.__lastHoverLatency || 120,
      domSnapshot: window.__domSnapshot || null,
    };
  };

  document.addEventListener('DOMContentLoaded', () => {
    attachHoverLatency();
    detectCssCollisions();
    applyMutation();
    renderNestedSubtasks();
    setTimeout(captureDom, 100);
  });
})();
