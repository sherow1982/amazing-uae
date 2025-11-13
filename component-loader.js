// Script to auto-load header and footer components
function loadComponent(selector, url) {
  fetch(url)
    .then(r => r.text())
    .then(html => {
      const container = document.querySelector(selector);
      if (container) {
        container.innerHTML = html;
      } else {
        // إذا لم يوجد عنصر بالسيليكتور، أنشئه أولاً
        const el = document.createElement('div');
        el.className = selector.replace('.','');
        el.innerHTML = html;
        if (selector === '.navbar' || selector === '.site-header') {
          document.body.insertAdjacentElement('afterbegin', el);
        } else {
          document.body.appendChild(el);
        }
      }
    });
}

// تحميل الهيدر والفوتر: ضع placeholders في صفحات المنتجات ب<div class="navbar"></div> و <div class="footer"></div>
document.addEventListener('DOMContentLoaded', function() {
    loadComponent('.navbar', 'header.html');
    loadComponent('.footer', 'footer.html');
});
