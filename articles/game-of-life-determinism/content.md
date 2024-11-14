Conway's Game of Life is a classic cellular automaton invented by the namesake mathematician John Conway in 1970. A flat, binary universe is spawned equipped with a handful of physical laws that dictate how the universe morphs from one moment of time to the next. We start by defining each cell to be dead (0) or alive (1). The  

# The Universe

<canvas id="game-of-life" width="332" height="332" style="display: block; margin: auto; border-radius: 4px;">
<div>
<button> &gt </button>
<button> &lt </button>
</div>
<script>
const canvas = document.getElementById("game-of-life");
const ctx = canvas.getContext("2d");
const cellSize = 30;
const p = 1;
const o = 1;
ctx.fillStyle="black";
ctx.fillRect(0,0,canvas.width,canvas.height);
ctx.fillStyle="white";
for (let x = 0; x < canvas.width; x += cellSize) {
    for (let y = 0; y < canvas.height; y += cellSize) {
        ctx.fillRect(x + o + p, y + o + p, cellSize - 2 * p, cellSize - 2 * p);
    }
}
</script>