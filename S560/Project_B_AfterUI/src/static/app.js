// Dynamic behavior, similar to Project A but with focused UX improvements
const list = document.querySelector('.task-list ul');
function addTask(title){
  const li = document.createElement('li');
  li.className = 'task-item';
  li.innerHTML = `<span class="icon">+</span><span class="title">${title}</span><button class="btn small">Edit</button>`;
  list.appendChild(li);
}

// add a dynamic verbose task to test reorder & spacing
setTimeout(()=>{addTask('Dynamic long title improved — polite spacing and wrapping with consistent baseline and reduced visual density');}, 700);

// improved hover styles via CSS; no additional JS necessary
