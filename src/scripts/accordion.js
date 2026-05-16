export function initAccordion() {
  const accordions = document.querySelectorAll('.accordion-item');
  
  accordions.forEach(item => {
    const trigger = item.querySelector('.accordion-trigger');
    const content = item.querySelector('.accordion-content');
    
    if (trigger && content) {
      trigger.addEventListener('click', () => {
        const isOpen = content.style.maxHeight;
        
        // Close all others
        accordions.forEach(otherItem => {
          const otherContent = otherItem.querySelector('.accordion-content');
          if (otherContent) {
            otherContent.style.maxHeight = null;
            otherItem.classList.remove('open');
          }
        });
        
        // Toggle current
        if (isOpen) {
          content.style.maxHeight = null;
          item.classList.remove('open');
        } else {
          content.style.maxHeight = content.scrollHeight + 'px';
          item.classList.add('open');
        }
      });
    }
  });
}
