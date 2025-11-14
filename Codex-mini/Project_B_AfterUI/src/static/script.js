const listEl = document.getElementById("task-list");
const statusText = {
  pending: "On Deck",
  "in-progress": "Active",
  blocked: "Blocked",
};

async function renderTasks() {
  try {
    const resp = await fetch("/api/tasks");
    const data = await resp.json();
    if (!Array.isArray(data)) {
      throw new Error("invalid payload");
    }
    listEl.innerHTML = data
      .map((task) => {
        const status = statusText[task.status] || "Pending";
        return `
        <article class="task-card" data-status="${task.status}">
          <div class="task-headline">
            <span class="task-icon" aria-hidden="true">${task.icon}</span>
            <div>
              <p class="task-title">${task.title}</p>
              <p class="task-category">${task.category}</p>
            </div>
            <span class="status-pill status-${task.status}">${status}</span>
          </div>
          <p class="task-note">${task.note || "Add context"}</p>
          <div class="actions">
            <button class="primary" aria-label="Plan ${task.title}">Plan</button>
            <button class="secondary" aria-label="See notes for ${task.title}">Notes</button>
          </div>
        </article>
      `;
      })
      .join("");
  } catch (err) {
    listEl.innerHTML = `<p class="task-note">Could not load tasks: ${err.message}</p>`;
  }
}

renderTasks();
