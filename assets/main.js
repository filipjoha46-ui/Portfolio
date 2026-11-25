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

  // Key figures (2700 K, 500 lm, 8.5 kg...) count up from zero when they scroll into view.
  // Only figures that start with a number animate; names like GX53 stay as they are.
  if(reduce||!('IntersectionObserver' in window)) return;
  document.querySelectorAll('.facts-row > div').forEach(function(box){
    var t=box.firstChild; if(!t||t.nodeType!==3) return;
    var m=t.nodeValue.match(/^(\d+(?:\.\d+)?)(.*)$/); if(!m) return;
    var end=parseFloat(m[1]),dec=(m[1].split('.')[1]||'').length,unit=m[2];
    var num=document.createElement('span'); num.className='count';
    num.textContent=m[1];
    box.replaceChild(num,t); box.insertBefore(document.createTextNode(unit),num.nextSibling);
    num.style.minWidth=num.getBoundingClientRect().width+'px';  // keep the width steady while digits change
    num.style.textAlign='right';
    num.textContent=(0).toFixed(dec);
    box._count=function(){
      var t0=null,dur=1600;
      function step(ts){if(t0===null)t0=ts;var u=Math.min(1,(ts-t0)/dur),e=1-Math.pow(1-u,3);
        num.textContent=(end*e).toFixed(dec); if(u<1) requestAnimationFrame(step);}
      requestAnimationFrame(step);
    };
  });
  var cio=new IntersectionObserver(function(entries){
    entries.forEach(function(en){if(!en.isIntersecting) return; cio.unobserve(en.target);
      en.target.querySelectorAll('.facts-row > div').forEach(function(b){if(b._count) b._count();});});
  },{threshold:.6});
  document.querySelectorAll('.facts-row').forEach(function(r){cio.observe(r)});
})();
