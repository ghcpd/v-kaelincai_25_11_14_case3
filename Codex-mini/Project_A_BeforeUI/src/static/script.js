const taskList = document.getElementById("task-list");

const STATUS_LABELS = {
  pending: "Awaiting",
  "in-progress": "In Flight",
  blocked: "Blocked",
};

async function loadTasks() {
  try {
    const response = await fetch("/api/tasks");
    const data = await response.json();
    renderTasks(data);
  } catch (err) {
    taskList.innerHTML = `<p class="error">Unable to load tasks.</p>`;
  }
}

function renderTasks(tasks) {
  if (!tasks || !Array.isArray(tasks)) {
    taskList.innerHTML = `<p class="empty">No tasks available.</p>`;
    return;
  }
  let html = "";
  tasks.forEach((task, index) => {
    const status = STATUS_LABELS[task.status] || "Unknown";
    const note = task.note ? `<p class="note">${task.note}</p>` : "";
    html += `<article class="task-card" data-index="${index}">
      <span class="task-icon">${task.icon || "?"}</span>
      <div>
        <p class="task-title">${task.title || "Untitled"}</p>
        <p class="task-category">${task.category || "general"}</p>
        ${note}
      </div>
      <span class="badge ${task.status}">${status}</span>
      <div class="task-actions">
        <button class="primary">Plan</button>
        <button class="secondary">Notes</button>
      </div>
    </article>`;
  });
  taskList.innerHTML = html;
}

loadTasks();
