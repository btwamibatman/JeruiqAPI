const track = document.getElementById("image-track");

window.onmousedown = e => {
    track.dataset.mouseDownAt = e.clientX;
}

window.onmouseup = () => {
    track.dataset.mouseDownAt = "0"; // Resets the mouse down position
}

window.onmousemove = e => {
    if (track.dataset.mouseDownAt === "0") return; // Prevents the function from running if mouse is not down

    const mouseDelta = parseFloat(track.dataset.mouseDownAt) - e.clientX,
            maxDelta = window.innerWidth / 2;

    const percentage = (mouseDelta / maxDelta) * -100;

    track.style.transform = `translate(${percentage}%, -50%)`;
}

// Mouse event handlers
window.onmousedown = e => handleOnDown(e);
window.onmouseup = e => handleOnUp();
window.onmousemove = e => handleOnMove(e);

// Touch event handlers - fixed to properly handle touch events
window.ontouchstart = e => handleOnDown(e.touches[0]);
window.ontouchend = e => handleOnUp(); // No parameter needed for touchend
window.ontouchmove = e => {
  if (e.touches && e.touches[0]) {
    handleOnMove(e.touches[0]);
  }
};