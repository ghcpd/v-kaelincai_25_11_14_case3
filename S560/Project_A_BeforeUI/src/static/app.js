// Minimal JS to allow simulated interactions
const list = document.querySelector('.task-list ul');
function addTask(title){
  const li = document.createElement('li');
  li.className = 'task-item';
  li.innerHTML = `<span class="icon">+</span><span class="title">${title}</span><button class="btn">Edit</button>`;
  list.appendChild(li);
}

// Example dynamic mutation to test nested DOM-handling
setTimeout(()=>{addTask('Dynamic Long Title that stress-tests layout by being very verbose and long to check overflow');}, 500);