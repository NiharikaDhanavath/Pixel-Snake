const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreDisplay = document.getElementById('score');

let gridSize = 20;
let tileSize = canvas.width / gridSize;
let snake = [{ x: 10, y: 10 }];
let direction = { x: 0, y: 0 };
let food = { x: Math.floor(Math.random() * gridSize), y: Math.floor(Math.random() * gridSize) };
let score = 0;

// Game loop
function gameLoop() {
  update();
  draw();
  if (isGameOver()) {
    alert('Game Over! Final Score: ' + score);
    resetGame();
  } else {
    setTimeout(gameLoop, 100);
  }
}

// Update game state
function update() {
  const head = { ...snake[0] };
  head.x += direction.x;
  head.y += direction.y;

  // Wrap around edges
  if (head.x < 0) head.x = gridSize - 1;
  if (head.x >= gridSize) head.x = 0;
  if (head.y < 0) head.y = gridSize - 1;
  if (head.y >= gridSize) head.y = 0;

  snake.unshift(head);

  // Check if food is eaten
  if (head.x === food.x && head.y === food.y) {
    score += 1;
    scoreDisplay.textContent = 'Score: ' + score;
    food = {
      x: Math.floor(Math.random() * gridSize),
      y: Math.floor(Math.random() * gridSize),
    };
  } else {
    snake.pop(); // Remove tail
  }
}

// Draw the game
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw food
  ctx.fillStyle = 'red';
  ctx.fillRect(food.x * tileSize, food.y * tileSize, tileSize, tileSize);

  // Draw snake
  ctx.fillStyle = 'lime';
  snake.forEach((segment) =>
    ctx.fillRect(segment.x * tileSize, segment.y * tileSize, tileSize, tileSize)
  );
}

// Check if the game is over
function isGameOver() {
  for (let i = 1; i < snake.length; i++) {
    if (snake[0].x === snake[i].x && snake[0].y === snake[i].y) {
      return true;
    }
  }
  return false;
}

// Reset the game
function resetGame() {
  snake = [{ x: 10, y: 10 }];
  direction = { x: 0, y: 0 };
  score = 0;
  scoreDisplay.textContent = 'Score: 0';
  food = { x: Math.floor(Math.random() * gridSize), y: Math.floor(Math.random() * gridSize) };
}

// Handle keyboard input
document.addEventListener('keydown', (e) => {
  switch (e.key) {
    case 'ArrowUp':
      if (direction.y === 0) direction = { x: 0, y: -1 };
      break;
    case 'ArrowDown':
      if (direction.y === 0) direction = { x: 0, y: 1 };
      break;
    case 'ArrowLeft':
      if (direction.x === 0) direction = { x: -1, y: 0 };
      break;
    case 'ArrowRight':
      if (direction.x === 0) direction = { x: 1, y: 0 };
      break;
  }
});

// Start the game
gameLoop();
