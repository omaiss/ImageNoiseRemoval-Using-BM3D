const divider = document.querySelector('.divider');
const scrollIcon = document.querySelector('.scroll-icon');
const container = document.querySelector('.container');
document.querySelector('.slider').addEventListener('input', (e) => {
  container.style.setProperty('--position', `${e.target.value}%`);
})
const images = document.querySelectorAll('.image-container img');
const verticalLine = document.querySelector('.vertical-line');
let isResizing = false;

divider.addEventListener('mousedown', function(e) {
    isResizing = true;
    document.addEventListener('mousemove', resize);
    document.addEventListener('mouseup', stopResize);
});

scrollIcon.addEventListener('mousedown', function(e) {
    document.addEventListener('mousemove', moveScrollIcon);
    document.addEventListener('mouseup', stopMovingScrollIcon);
});

function resize(e) {
    if (isResizing) {
        const offset = container.getBoundingClientRect().left;
        const newX = e.clientX - offset;
        divider.style.left = newX + 'px';
        divider.style.transition = 'none';
        divider.style.pointerEvents = 'auto';
        divider.style.cursor = 'ew-resize';

        container.style.width = newX + 'px';
    }
}


function stopResize() {
    isResizing = false;
    document.removeEventListener('mousemove', resize);
    divider.style.transition = 'all 0.2s ease';
    divider.style.pointerEvents = 'auto';
    divider.style.cursor = 'ew-resize';
}

function moveScrollIcon(e) {
    const containerRect = container.getBoundingClientRect();
    const containerWidth = containerRect.width;
    const mouseX = e.clientX - containerRect.left;

    const percent = mouseX / containerWidth;

    const iconWidth = scrollIcon.offsetWidth;
    const halfIconWidth = iconWidth / 2;
    let newX = mouseX - halfIconWidth;
    if (newX < 0) newX = 0;
    if (newX > containerWidth - iconWidth) newX = containerWidth - iconWidth;

    scrollIcon.style.left = newX + 'px';
    verticalLine.style.left = newX + 'px';

    const leftWidth = newX + halfIconWidth;
    const rightWidth = containerWidth - leftWidth;

    container.style.width = containerWidth + 'px';
    images[0].style.width = leftWidth + 'px';
    images[1].style.width = rightWidth + 'px';

    e.preventDefault();
}

function stopMovingScrollIcon() {
    document.removeEventListener('mousemove', moveScrollIcon);
}

