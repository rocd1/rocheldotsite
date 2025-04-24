document.addEventListener('DOMContentLoaded', function() {
    const content = document.getElementById('lessonContent');
    const button = document.getElementById('toggleButton');

    button.addEventListener('click', function() {
        // Check if content is currently expanded or collapsed
        if (content.style.maxHeight === 'none') {
            content.style.maxHeight = '150px'; // Collapse the content
            content.style.overflowY = 'hidden';
            button.innerText = 'See More';
        } else {
            content.style.maxHeight = 'none'; // Expand the content
            content.style.overflowY = 'visible';
            button.innerText = 'See Less';
        }
    });
});


