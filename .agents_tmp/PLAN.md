# 1. OBJECTIVE
Скопировать все страницы с оригинального сайта ttevents.ru (около 70 страниц), создать новый современный адаптивный дизайн, очистить проект от лишних файлов.

# 2. CONTEXT SUMMARY
* Текущий проект: HTML-сайт event-агентства TT Events в /workspace/project/ttevents-ru/ttevents/
* Оригинальный сайт: https://ttevents.ru (около 70 страниц согласно sitemap.xml)
* Структура: HTML-страницы + папки g/, t/, thumb/, shared/ с ресурсами
* Задача: Полная копия с чисткой + новый дизайн

# 3. APPROACH OVERVIEW
1. Скачать все страницы с ttevents.ru через fetch/crawl
2. Очистить старые HTML-файлы от мусора
3. Создать новый современный адаптивный дизайн (CSS + HTML)
4. Сохранить пути как на оригинале для SEO
5. Удалить лишние ресурсы (g/, t/, thumb/)

# 4. IMPLEMENTATION STEPS

## Шаг 1: Получить список всех страниц для скачивания
**Цель**: Определить полный список URL для копирования
**Метод**: Использовать sitemap.xml как список страниц
**Справка**: ttevents/sitemap.xml (78 страниц)

## Шаг 2: Скачать контент страниц (полный список)
**Цель**: Получить контент со всех страниц
**Метод**: tavily_extract для каждой страницы (последовательно)
**Список страниц для скачивания:**

### Основные страницы (главные разделы):
1. https://ttevents.ru/ (главная)
2. https://ttevents.ru/o-nas
3. https://ttevents.ru/delovye-meropriyatiya
4. https://ttevents.ru/sportivnye-meropriyatiya
5. https://ttevents.ru/turisticheskie-i-ekskursionnye-meropriyatiya
6. https://ttevents.ru/timbilding-moskva
7. https://ttevents.ru/gosudarstvennye-prazdniki
8. https://ttevents.ru/master-klassy
9. https://ttevents.ru/immersivnyj-korporativ
10. https://ttevents.ru/festivali
11. https://ttevents.ru/onlajn-meropriyatiya
12. https://ttevents.ru/intellektualnye-igry
13. https://ttevents.ru/party
14. https://ttevents.ru/classic
15. https://ttevents.ru/art-korporativ
16. https://ttevents.ru/aktivnye-timbildingi
17. https://ttevents.ru/kreativnye-timbildingi
18. https://ttevents.ru/kvesty-i-igry
19. https://ttevents.ru/konferencii-i-forumy
20. https://ttevents.ru/strategicheskie-sessii-i-vorkshopy
21. https://ttevents.ru/prezentacii-novyh-produktov-launch-events
22. https://ttevents.ru/seminary-i-treningi
23. https://ttevents.ru/mice-delovoj-turizm
24. https://ttevents.ru/festivaly-i-gorodskie-meropriyatiya

### Кейсы (case):
25. https://ttevents.ru/case
26. https://ttevents.ru/case/mediaproekt-i-fotovystavka-supersila
27. https://ttevents.ru/case/den_nko_2024
28. https://ttevents.ru/case/nad-moskvoy-zarya
29. https://ttevents.ru/case/vremena-goda
30. https://ttevents.ru/case/ek-park
31. https://ttevents.ru/case/imersivny-thatr
32. https://ttevents.ru/case/korolevsky-novy-god-24
33. https://ttevents.ru/case/maslenitsa-izmaylovo25case
34. https://ttevents.ru/case/eho-pobedy-ope-air-2025
35. https://ttevents.ru/case/9may
36. https://ttevents.ru/case/lauch-event-umg
37. https://ttevents.ru/case/open-air-slava-skripka-bober-2025
38. https://ttevents.ru/case/vremnadezhdfest2025
39. https://ttevents.ru/case/artpop
40. https://ttevents.ru/case/art-novy-god-otel-svezhy-veter-2026

### Блог:
41. https://ttevents.ru/blog
42. https://ttevents.ru/blog/organizatsiya-korporativov-moskva-2026
43. https://ttevents.ru/blog/3-trenda
44. https://ttevents.ru/blog/korporativ-na-9-maya-2026-v-moskve
45. https://ttevents.ru/blog/pochemu-russkie-narodnye-motivy-populyarny
46. https://ttevents.ru/blog/korporativ-na-9-maya-dlya-kompanii-12-idej-meropriyatij-ko-dnyu-pobedy-scenarii-i-formaty-2026
47. https://ttevents.ru/blog/kak-provesti-launch-event-10-formatov-prezentacii-novogo-produkta
48. https://ttevents.ru/blog/it-corporativ
49. https://ttevents.ru/blog/it-corporativ-idei
50. https://ttevents.ru/blog/kak-vybrat-event-agentstvo-v-moskve

### Остальные:
51. https://ttevents.ru/videoproduction
52. https://ttevents.ru/video-portfolio
53. https://ttevents.ru/novogodniy-korporativ
54. https://ttevents.ru/letnij-korporativ
55. https://ttevents.ru/korporativ-na-prirode
56. https://ttevents.ru/timbilding-na-prirode
57. https://ttevents.ru/yubilej-kompanii
58. https://ttevents.ru/mediaproekty
59. https://ttevents.ru/event-agentstvo-moskva
60. https://ttevents.ru/korporativy-moskva
61. https://ttevents.ru/organizaciya-meropriyatij-v-moskve
62. https://ttevents.ru/tendery

## Шаг 2.1: Скачать картинки и видео
**Цель**: Сохранить все медиафайлы (изображения, видео)
**Метод**: Найти все img src и video source в контенте, скачать файлы
**Справка**: thumb/, images/ - пути как на оригинале

## Шаг 3: Очистить старые HTML-файлы
**Цель**: Удалить старые HTML-файлы перед созданием новых
**Метод**: Удалить все .html файлы (кроме index.html если нужен)
**Справка**: ttevents/*.html

## Шаг 4: Создать новые HTML-файлы с контентом
**Цель**: Создать HTML-файлы с контентом и новым дизайном
**Метод**: 
- Использовать полученный контент из шага 2
- Применить современный адаптивный CSS-шаблон
- Сохранить пути как на оригинале
**Справка**: По одному файлу на каждую страницу

## Шаг 5: Создать CSS нового дизайна
**Цель**: Современный адаптивный дизайн
**Метод**: 
- CSS переменные для цветов
- Flexbox/Grid для layout
- Медиа-запросы для адаптивности
- Современная типографика
**Справка**: ttevents/css/style.css (новый файл)

## Шаг 6: Очистить ресурсы (g/, t/, thumb/)
**Цель**: Удалить все лишние файлы ресурсов
**Метод**: Удалить папки g/, t/, thumb/ (или оставить только минимум)
**Справка**: ttevents/g/, ttevents/t/, ttevents/thumb/

## Шаг 7: Проверить работоспособность
**Цель**: Убедиться что всё работает
**Метод**: Проверить главную страницу через браузер
**Результат**: Страница открывается без ошибок

# 5. TESTING AND VALIDATION
* Все ~78 страниц скопированы и доступны
* Пути совпадают с оригиналом
* Новый дизайн адаптивный (mobile/tablet/desktop)
* Лишние файлы удалены
* Главная страница открывается корректно
