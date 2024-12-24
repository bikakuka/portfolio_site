// Получаем элементы модального окна и кнопки
const modal = document.getElementById('modal');
const openModalBtn = document.getElementById('openModalBtn');
const closeModalBtn = document.getElementById('closeModalBtn');

// Открыть модальное окно при нажатии на кнопку
openModalBtn.addEventListener('click', () => {
    modal.style.display = 'block';
});

// Закрыть модальное окно при нажатии на крестик
closeModalBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Закрыть модальное окно при клике вне его области
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});