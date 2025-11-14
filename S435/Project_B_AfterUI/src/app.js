// Improved interactions: hover/active, keyboard accessible focus styles, aria labeling
window.addEventListener('load', function(){
  const list = document.getElementById('task-list');
  document.querySelectorAll('.btn').forEach(b=>{
    b.addEventListener('click', function(e){
      const t = e.target.closest('.task');
      if(t){
        t.classList.toggle('done');
        b.setAttribute('aria-pressed', t.classList.contains('done'));
        t.style.opacity = t.classList.contains('done') ? '0.6' : '1';
      }
    });
    b.addEventListener('keydown', function(e){
      if(e.key === 'Enter' || e.key === ' '){ b.click(); }
    });
  });
});
