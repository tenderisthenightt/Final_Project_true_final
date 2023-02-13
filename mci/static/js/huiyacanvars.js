// app.js
const canvas = document.getElementById("jsCanvas");
const ctx = canvas.getContext("2d");
const brush = document.getElementById("jsBrush");
const erase = document.getElementById("jsErase");
const submitButton = document.getElementById("jsSubmitButton");

// send image
submitButton.addEventListener("click", function () {
    const dataURL = canvas.toDataURL();
    const formData = new FormData();
    formData.append("file(여기바꾸기)", dataURLToFile(dataURL, "image.png"));
    const form = document.getElementById("form");
    form.submit();
});

function dataURLToFile(dataURL, fileName) {
    const byteString = atob(dataURL.split(",")[1]);
    const mimeString = dataURL.split(",")[0].split(":")[1].split(";")[0];
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new File([ab], fileName, { type: mimeString });
}

const INITIAL_COLOR = "#2c2c2c";
const INITIAL_LINEWIDTH = 5.0;
const CANVAS_SIZE = 500;

ctx.strokeStyle = INITIAL_COLOR;
ctx.fillStyle = INITIAL_COLOR;
ctx.lineWidth = INITIAL_LINEWIDTH;
canvas.width = CANVAS_SIZE;
canvas.height = CANVAS_SIZE;

const MODE_BUTTON = [brush, erase];
let mode = brush;
let painting = false;

function startPainting() { painting = true; }
function stopPainting() { painting = false; }

function onMouseMove(event) {
    // get the current size of the canvas
    let width = canvas.width;
    let height = canvas.height;

    // get the position of the mouse relative to the canvas
    let x = event.offsetX;
    let y = event.offsetY;

    // Scale the mouse coordinates based on the current canvas size
    x = x * width / canvas.offsetWidth;
    y = y * height / canvas.offsetHeight;

    ctx.lineWidth = 3.5;
    if(mode === brush){
        if(!painting) {
            ctx.beginPath();
            ctx.moveTo(x, y);
        }
        else {
            ctx.lineTo(x, y);
            ctx.stroke();
        }
    }
    // else if(mode === erase){
    //     if(painting) {
    //         ctx.clearRect(x-ctx.lineWidth/2, y-ctx.lineWidth/2, ctx.lineWidth, ctx.lineWidth);
    //     }
    // }
}

function handleModeChange(event) {
    mode = event.target;
    // Button Highlight
    for(i = 0 ; i < MODE_BUTTON.length ; i++){
        var button = MODE_BUTTON[i];
        if(button === mode){
            button.style.backgroundColor = "skyblue";
        }
        else {
            button.style.backgroundColor = "white";
        }
    }
}

function handleStart(event) {
    // Mouse down event or touch start event
    painting = true;
    let x, y;
    if (event.type === "mousedown") {
      x = event.offsetX;
      y = event.offsetY;
    } else {
      x = event.touches[0].clientX - canvas.offsetLeft;
      y = event.touches[0].clientY - canvas.offsetTop;
    }
    ctx.beginPath();
    ctx.moveTo(x, y);
  }
  
  function handleMove(event) {
    if (!painting) return;
    let x, y;
    if (event.type === "mousemove") {
      x = event.offsetX;
      y = event.offsetY;
    } else {
      x = event.touches[0].clientX - canvas.offsetLeft;
      y = event.touches[0].clientY - canvas.offsetTop;
    }
    ctx.lineTo(x, y);
    ctx.stroke();
  }
  
  function handleEnd(event) {
    // Mouse up event or touch end event
    painting = false;
  }
  
  if (canvas) {
    canvas.addEventListener("mousedown", handleStart);
    canvas.addEventListener("mousemove", handleMove);
    canvas.addEventListener("mouseup", handleEnd);
    canvas.addEventListener("mouseleave", handleEnd);
    canvas.addEventListener("touchstart", handleStart);
    canvas.addEventListener("touchmove", handleMove);
    canvas.addEventListener("touchend", handleEnd);
  }

// All Remove Bts

jsAllremove.addEventListener("click", () => ctx.clearRect(0, 0, canvas.width, canvas.height));

if (canvas) {
    canvas.addEventListener("mousemove", onMouseMove);
    canvas.addEventListener("mousedown", startPainting);
    canvas.addEventListener("mouseup", stopPainting);
    canvas.addEventListener("mouseleave", stopPainting);
}

MODE_BUTTON.forEach(mode => mode.addEventListener("click", handleModeChange)
);