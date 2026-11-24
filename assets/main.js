// Fade-in on scroll and reduced-motion handling
(function(){
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var els=document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);}});
    },{rootMargin:'0px 0px -8% 0px'});
    els.forEach(function(e){io.observe(e)});
  } else { els.forEach(function(e){e.classList.add('in')}); }
  if(reduce){document.querySelectorAll('video[autoplay]').forEach(function(v){v.removeAttribute('autoplay');v.pause();});}
  var y=document.getElementById('year'); if(y) y.textContent=new Date().getFullYear();
})();
