/**
 * Analytics с consent management
 */
export function initAnalytics() {
  // Google Analytics 4
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('config', 'G-XD0H7W05XN');
  
  // Yandex Metrika
  (function(m,e,t,r,i,k,a){
    m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
    m[i].l=1*new Date();
    k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
  })(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=106696326', 'ym');
  
  ym(106696326, 'init', {ssr:true, webvisor:true, clickmap:true});
}
