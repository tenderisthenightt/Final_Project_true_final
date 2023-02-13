// Constant
const INITIAL_COLOR = '#2c2c2c'
const INITIAL_BG_COLOR = 'white';
const INITIAL_LINE_WIDTH = 2.5;
const BTN_CLICKED_CN = 'controls__color__clicked';
// Dom Element

const canvasParent = document.querySelector('#canvas');
const canvas = document.querySelector("#jsCanvas");
const ctx = canvas.getContext('2d');
const colors = document.querySelectorAll('.jsColor')
const myColorContorls = document.querySelector('#jsMyColorControl');
const myColor = document.querySelector('#jsMyColor')
const range = document.querySelector('#jsRange');
const mode = document.querySelector('#jsMode');
const saveBtn = document.querySelector('#jsSave');
// const Btn = document.querySelector('#jsMove');
const resetBtn = document.querySelector('#jsReset');
const resizeBtn = document.querySelector('#jsResize');
const widthControls = document.querySelector('#jsWidth');
const heightControls = document.querySelector('#jsHeight');

// 이미지 보내기


// Variable

// !! 사이즈 조절함
let canvasWidth = 820;
let canvasHeight = 400;
let isPainting = false;
let isFilling = false;
// Init setting
const initSetting = () => {
  // Set width, height of canvas
  
  canvas.width = canvasWidth;
  canvas.height = canvasHeight;
  // Set background color, paint color, fill color, line width of canvas
  ctx.fillStyle = INITIAL_BG_COLOR;
  ctx.fillRect(0, 0, canvasWidth, canvasHeight);
  ctx.strokeStyle = INITIAL_COLOR;
  ctx.fillStyle = INITIAL_COLOR;
  ctx.lineWidth = INITIAL_LINE_WIDTH;
  // Set initial line width
  range.value = INITIAL_LINE_WIDTH;
  // Set initial mode to paint
  isFilling = false;
  mode.innerText = 'fill';
  // Set all button unclicked
  colors.forEach(color=>{
    color.classList.remove(BTN_CLICKED_CN);
  })
  // Set black button clicked
  colors[0].classList.add(BTN_CLICKED_CN);
}
// Init event
const initEvent = () => {
  // Add event to Canvas
  if (canvas) {
    canvas.addEventListener("mousemove", onMouseMove);
    canvas.addEventListener("mouseleave", stopPainting);
    canvas.addEventListener("mouseup", stopPainting);
    canvas.addEventListener("mousedown", startPainting);
    canvas.addEventListener("click", handleCanvasClick);
    canvas.addEventListener("contextmenu", handleContextMenu)
  }
  // Add event to color
  colors.forEach(color => {
    color.addEventListener('click', handleColorClick);
  })
  // Add event to range
  if (range) {
    range.addEventListener("input", handleRangeChange);
  }
  // Add event to mode button
  if (mode) {
    mode.addEventListener("click", hanldeModeClick);
  }
  // Add event to save button
  if (saveBtn) {
    saveBtn.addEventListener("click", handleSaveClick);
  }
  // Add event to reset button
  if (resetBtn) {
    resetBtn.addEventListener("click", handleResetClick);
  }
  // Add event to my color
  if (myColorContorls) {
    myColorContorls.addEventListener("change", handleMyColorChange);
  }
  // Add event to resize button
  if (resizeBtn) {
    resizeBtn.addEventListener("click", handleResizeClick);
  }
}
// Set start paint
const startPainting = () => {
  isPainting = true;
}
// Set stop paint
const stopPainting = () => {
  isPainting = false;
}
// Event of move mouse on canvas
const onMouseMove = (e) => {
  if (isFilling)
    return;
  const x = e.offsetX;
  const y = e.offsetY;
  if (!isPainting) {
    ctx.beginPath();
    ctx.moveTo(x, y);
  } else {
    ctx.lineTo(x, y);
    ctx.stroke();
  }
}
// Event of click color
const handleColorClick = (e) => {
  // set color of paint or fill
  const color = e.target.style.backgroundColor;
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  // Set all button unclicked
  colors.forEach(color=>{
    color.classList.remove(BTN_CLICKED_CN);
  })
  // Set clicked button clicked
  e.target.classList.add(BTN_CLICKED_CN);
}
// Event of change line width
const handleRangeChange = (e) => {
  const size = e.target.value;
  ctx.lineWidth = size;
}
// Event of change mode
const hanldeModeClick = () => {
  if (isFilling === true) {
    // If current mode is paint
    isFilling = false;
    mode.innerText = 'fill';
  } else {
    // If current mode is fill
    isFilling = true;
    mode.innerText = 'paint';
  }
}
// Event of click canvas
const handleCanvasClick = () => {
  if (isFilling === true) {
    ctx.fillRect(0, 0, canvasWidth, canvasHeight);
  }
}
// Prevent event of right click
const handleContextMenu = (e) => {
  e.preventDefault();
}
// Event of Click save button
const handleSaveClick = () => {
  const image = canvas.toDataURL();
  const link = document.createElement('a');
  link.href = image;
  link.download = '글,그림 검사';
  link.click();
}
// // Event of Click move button(이미지 이동)
// document.getElementById("save-btn").addEventListener("click", function() {
//   let canvas = document.getElementById("jsCanvas");
//   let dataURL = canvas.toDataURL();
//   let xhr = new XMLHttpRequest();
//   xhr.open("POST", "/predict", true);
//   xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
//   xhr.send("image=" + dataURL);
// });

// Event of Click reset button
const handleResetClick = () => {
  initSetting();
}
// Event of Change my color
const handleMyColorChange = (e) => {
  const color = e.target.value;
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  myColor.style.backgroundColor = color;
}
// Event of Change size of canvas
const handleResizeClick = (e) => {
  if (widthControls.value>window.innerWidth){
    alert('Too Large');
  }else{
    canvasWidth = widthControls.value;
    canvasHeight = heightControls.value;
    initSetting();
  }
}
// init
initSetting();
initEvent();

// 사이즈 조절

// important! for alignment, you should make things
// relative to the canvas' current width/height.

function draw() {
    var ctx = (canvas);
    ctx.canvas.width  = window.innerWidth;
    ctx.canvas.height = window.innerHeight;
    //...drawing code...
  }