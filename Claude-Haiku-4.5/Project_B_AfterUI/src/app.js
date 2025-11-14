// AFTER: Enhanced task list with smooth interactions
document.addEventListener('DOMContentLoaded', function() {
    const taskInput = document.getElementById('taskInput');
    const addBtn = document.getElementById('addBtn');
    const taskList = document.getElementById('taskList');

    addBtn.addEventListener('click', addTask);
    taskInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addTask();
        }
    });

    // Delete and toggle functionality
    document.addEventListener('click', function(e) {
        if (e.target.closest('.delete-btn')) {
            e.target.closest('.task-item').remove();
        } else if (e.target.classList.contains('task-checkbox')) {
            e.target.closest('.task-item').classList.toggle('completed');
        }
    });

    function addTask() {
        const taskText = taskInput.value.trim();
        if (!taskText) {
            return;
        }

        const li = document.createElement('li');
        li.className = 'task-item';
        li.setAttribute('role', 'listitem');
        li.innerHTML = `
            <input type="checkbox" class="task-checkbox" aria-label="Mark task complete">
            <span class="task-title">${escapeHtml(taskText)}</span>
            <button class="delete-btn" aria-label="Delete task">
                <span class="icon">✕</span>
            </button>
        `;
        
        taskList.appendChild(li);
        taskInput.value = '';
        taskInput.focus();
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
