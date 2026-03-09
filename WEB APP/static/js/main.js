// static/js/main.js
// tilt/hover on tiles and headline observer + small helpers
document.addEventListener('DOMContentLoaded', ()=>{
  // tilt on data-tilt tiles
  const tiles = document.querySelectorAll('[data-tilt]');
  tiles.forEach(tile=>{
    tile.addEventListener('mousemove', (e)=>{
      const rect = tile.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width;
      const y = (e.clientY - rect.top) / rect.height;
      const rx = (y - 0.5) * 10;
      const ry = (x - 0.5) * -12;
      tile.style.transform = `translate(-50%,-50%) rotateX(${rx}deg) rotateY(${ry}deg) scale(1.02)`;
    });
    tile.addEventListener('mouseleave', ()=>{ tile.style.transform = 'translate(-50%,-50%) scale(1)'; });
  });

  // headline IntersectionObserver
  const h = document.getElementById('bigHeadline');
  if(h){
    const io = new IntersectionObserver(entries=>{
      entries.forEach(e=>{ if(e.isIntersecting) h.style.animation = 'slideIn 1200ms cubic-bezier(.22,.9,.31,1) 0ms forwards'; });
    }, {threshold:0.2});
    io.observe(h);
  }

  // parallax media stage
  const mediaStage = document.getElementById('mediaStage');
  window.addEventListener('scroll', ()=>{
    if(!mediaStage) return;
    const rect = mediaStage.getBoundingClientRect();
    const mid = rect.top + rect.height/2 - window.innerHeight/2;
    const t = Math.max(-1, Math.min(1, -mid / (window.innerHeight/1.8)));
    mediaStage.style.transform = `translateY(${t * 12}px)`;
  }, {passive:true});
});

// small helper for navigation
function scrollToSection(sel){ const el = document.querySelector(sel); if(!el) return; el.scrollIntoView({behavior:'smooth', block:'start'}); }