// BEFORE: Basic task list app without enhancements
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

    // Delete functionality
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-btn')) {
            e.target.parentElement.remove();
        }
    });

    function addTask() {
        const taskText = taskInput.value.trim();
        if (!taskText) {
            return;
        }

        const li = document.createElement('li');
        li.className = 'task-item';
        li.innerHTML = `
            <input type="checkbox" class="task-checkbox">
            <span class="task-title">${escapeHtml(taskText)}</span>
            <button class="delete-btn">x</button>
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
