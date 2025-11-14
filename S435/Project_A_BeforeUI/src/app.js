// Baseline JS: minimal, no interaction or hover feedback
window.addEventListener('load', function(){
  const list = document.getElementById('task-list');
  list.addEventListener('click', function(e){
    if(e.target.tagName === 'BUTTON'){
      const t = e.target.closest('.task');
      if(t) t.style.opacity = 0.6;
    }
  });
});
