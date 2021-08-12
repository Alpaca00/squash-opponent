
const jail = document.getElementById('jail');

document.addEventListener('mousemove', mouseUpdate, false);
document.addEventListener('mouseenter', mouseUpdate, false);

const seenMouse = false;

function mouseUpdate(e) {
  const jailCoords = jail.getBoundingClientRect();
  const pageCoords = document.body.getBoundingClientRect();

  const x = e.pageX - jailCoords.left;
  const y = e.pageY - jailCoords.top;

  document.body.style.setProperty('--mouseX', x);
  document.body.style.setProperty('--mouseY', y);

  document.body.style.setProperty('--width', pageCoords.width);
  document.body.style.setProperty('--height', pageCoords.height);

  if (!seenMouse) {
    document.body.classList.add('seenMouse');
    seenMouse = true;
  }
}

function mouseLeft(e) {
  document.body.classList.remove('seenMouse');
  seenMouse = false;
}

document.addEventListener('mouseleave', mouseLeft, false);
