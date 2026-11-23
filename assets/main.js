// Fade-in on scroll + pause hero film for reduced motion
(function(){
  var els=document.querySelectorAll('.reveal');
  if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in')});return;}
  var io=new IntersectionObserver(function(entries){
    entries.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);}});
  },{rootMargin:'0px 0px -8% 0px'});
  els.forEach(function(e){io.observe(e)});
  var v=document.querySelector('video[data-hero]');
  if(v&&window.matchMedia('(prefers-reduced-motion: reduce)').matches){v.removeAttribute('autoplay');v.pause();}
  var y=document.getElementById('year');if(y)y.textContent=new Date().getFullYear();
})();
