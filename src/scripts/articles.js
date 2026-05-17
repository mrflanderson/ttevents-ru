/**
 * Скрипты для страниц статей (блог, кейсы)
 * Добавляет "Читать далее" ссылки
 */
export function initArticleReadMore() {
  // Ищем все карточки статей
  const articles = document.querySelectorAll('.article-card, .case-card');
  
  articles.forEach(article => {
    // 1. Находим ссылку на полную статью (она в заголовке)
    const titleElement = article.querySelector('.article-title, .case-title');
    let articleUrl = null;
    
    if (titleElement && titleElement.tagName === 'A') {
      articleUrl = titleElement.href; // Сам заголовок — ссылка
    } else {
      const linkInside = titleElement?.querySelector('a');
      if (linkInside) articleUrl = linkInside.href; // Ссылка внутри заголовка
    }
    
    // Если ссылка не нашлась, ищем любую первую ссылку в карточке
    if (!articleUrl) {
      const anyLink = article.querySelector('a[href]');
      if (anyLink) articleUrl = anyLink.href;
    }
    
    // 2. Находим блок с текстом, куда будем вставлять ссылку
    const textBlock = article.querySelector('.article-card-content, .case-card-content');
    
    // 3. Если всё найдено и ссылки еще нет — добавляем
    if (articleUrl && textBlock && !textBlock.querySelector('.read-more')) {
      const readMoreLink = document.createElement('span');
      readMoreLink.className = 'read-more';
      readMoreLink.textContent = 'Читать далее →';
      readMoreLink.style.cursor = 'pointer';
      readMoreLink.style.textDecoration = 'underline';
      
      // Добавляем обработчик клика
      readMoreLink.addEventListener('click', (e) => {
        e.preventDefault();
        window.location.href = articleUrl;
      });
      
      // Вставляем ссылку в конец текстового блока
      textBlock.appendChild(readMoreLink);
    }
  });
}

// Запускаем при загрузке
document.addEventListener('DOMContentLoaded', initArticleReadMore);
