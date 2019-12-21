//credits for the base of the interaction-handling logic:
//https://dzone.com/articles/gentle-introduction-making
//rest by Nil M.

//X grows to the right and Y grows upwards(?)
var canvasSize = document.getElementById('canvas1').offsetWidth-2;
var canvasOffset = 1;
var maxCanvasSize = 700;
var maxCellSize = 30;

//HTML canvas coordinate system:
//The first coordinate (X) grows to the right
//The second coordinate (Y) grows downwards
//Chess board coordinate system:
//The first coordinate (i) grows downwards
//The second coordinate (j) grows to the right

//trasform chees coordinate to canvas coordinate
//(to the point at the center of the cell)
function xPos(j, w, canvasJSize) {
  let cellLength = canvasJSize/w;
  return canvasOffset + j*cellLength + 0.5*cellLength;
}

function yPos(i, h, canvasISize) {
  let cellLength = canvasISize/h;
  return canvasOffset + i*cellLength + 0.5*cellLength;
}

//knight moves (clockwise order starting at 12):
//0: 2-up 1-right, 1: 1-up 2-right, 2: 1-down 2-right, 3: 2-down 1-right
//4: 2-down 1-left, 5: 1-down 2-left, 6: 1-up 2-left, 7: 2-up 1-left
var movesI = [-2,-1, 1, 2, 2, 1,-1,-2];
var movesJ = [1,  2, 2, 1,-1,-2,-2,-1];

var CornerHMatchHeight5 = [ //6x5
'02 37 xx xx xx xx',
'03 47 26 23 xx xx',
'23 24 47 23 36 46',
'02 27 56 26 57 56',
'01 07 16 16 07 67']

var CornerVMatchHeight5 = [ //6x5
'03 27 xx xx xx xx',
'03 47 45 26 xx xx',
'13 47 23 23 35 46',
'02 07 15 25 56 56',
'01 17 16 17 07 67']

var CornerVMatchHeight6 = [ //8x6
'03 27 xx xx xx xx xx xx',
'02 27 24 26 xx xx xx xx',
'23 47 26 26 26 26 xx xx',
'23 04 26 34 26 26 36 46',
'02 27 56 25 26 25 56 56',
'01 17 06 16 17 16 06 67']

var CornerVMatchHeight7 = [ //10x7
'02 27 xx xx xx xx xx xx xx xx',
'02 27 26 26 xx xx xx xx xx xx',
'23 24 26 26 26 26 xx xx xx xx',
'23 24 26 26 26 26 26 26 xx xx',
'03 47 26 26 46 36 26 26 36 46',
'02 27 25 25 56 26 25 25 56 56',
'01 17 16 06 16 16 17 16 06 67']

var CornerVMatchHeight8 = [ //12x8
'02 27 xx xx xx xx xx xx xx xx xx xx',
'02 27 26 26 xx xx xx xx xx xx xx xx',
'23 24 26 26 26 26 xx xx xx xx xx xx',
'23 24 26 26 26 26 26 26 xx xx xx xx',
'03 37 26 26 56 26 26 26 26 26 xx xx',
'03 47 15 23 46 26 45 46 26 26 36 46',
'12 27 57 25 15 26 25 26 25 25 56 56',
'01 17 16 06 17 06 01 16 16 16 06 67']

var VerticalEdge = [ //2x4
'23 24',
'23 24',
'02 27',
'02 27'];

var Sequence1 = [ //8x4 (heel)
'36 46 26 26 26 26 xx xx',
'36 46 23 24 26 26 36 46',
'02 27 25 25 26 26 56 56',
'01 17 06 67 16 16 06 67'];

var Sequence0 = [ //6x4
'36 46 26 26 36 46',
'36 46 23 24 36 46',
'02 27 25 25 06 67',
'01 17 06 67 06 67'];

var Sequence2part2 = [ //4x6
'26 26 36 46',
'36 46 36 46',
'36 46 03 47',
'03 47 03 47',
'02 27 05 57',
'01 17 06 67'];

var Sequence3 = [ //4x6
'26 26 36 46',
'36 46 36 46',
'36 46 03 47',
'02 27 05 57',
'01 17 06 67'];

var flippedSequence3 = [ //delete if not used
'23 24 35 45',
'13 14 36 46',
'03 47 02 27',
'02 27 02 27',
'02 27 26 26'];



function CanvasState(canvas) {

  // **** First some setup! ****
  this.canvas = canvas;
  this.width = canvas.width;
  this.height = canvas.height;
  this.ctx = canvas.getContext('2d');
  // This complicates things a little but fixes mouse co-ordinate problems
  // when there's a border or padding. See getMouse for more detail
  var stylePaddingLeft, stylePaddingTop, styleBorderLeft, styleBorderTop;
  if (document.defaultView && document.defaultView.getComputedStyle) {
    this.stylePaddingLeft = parseInt(document.defaultView.getComputedStyle(canvas, null)['paddingLeft'], 10)      || 0;
    this.stylePaddingTop  = parseInt(document.defaultView.getComputedStyle(canvas, null)['paddingTop'], 10)       || 0;
    this.styleBorderLeft  = parseInt(document.defaultView.getComputedStyle(canvas, null)['borderLeftWidth'], 10)  || 0;
    this.styleBorderTop   = parseInt(document.defaultView.getComputedStyle(canvas, null)['borderTopWidth'], 10)   || 0;
  }
  // Some pages have fixed-position bars (like the stumbleupon bar) at the top or left of the page
  // They will mess up mouse coordinates and this fixes that
  var html = document.body.parentNode;
  this.htmlTop = html.offsetTop;
  this.htmlLeft = html.offsetLeft;

  // **** Keep track of state! ****

  this.valid = false; // when set to false, the canvas will redraw everything
  this.tour = genTour(30, 30);

  // **** Then events! ****

  // This is an example of a closure!
  // Right here "this" means the CanvasState. But we are making events on the Canvas itself,
  // and when the events are fired on the canvas the variable "this" is going to mean the canvas!
  // Since we still want to use this particular CanvasState in the events we have to save a reference to it.
  // This is our reference!
  var myState = this;

  //options
  this.interval = 30;
  setInterval(function() { myState.draw(); }, myState.interval);

  //fixes a problem where double clicking causes text to get selected on the canvas
  canvas.addEventListener('selectstart', function(e) { e.preventDefault(); return false; }, false);
}

CanvasState.prototype.clear = function() {
  this.ctx.clearRect(0, 0, this.width, this.height);
}

CanvasState.prototype.resize = function(h, w) {
  this.ctx.width = w+2*canvasOffset;
  this.ctx.height = h+2*canvasOffset;
}

// While draw is called as often as the INTERVAL variable demands,
// It only ever does something if the canvas gets invalidated by our code
CanvasState.prototype.draw = function() {
  // if our state is invalid, redraw and validate!
  if (this.valid) return;

  var ctx = this.ctx;
  var tour = this.tour;
  var height = tour.length;
  var width = tour[0].length;
  let canvasCellSize = Math.min(maxCellSize, Math.min(maxCanvasSize/height, maxCanvasSize/width))
  let canvasISize = canvasCellSize*height;
  let canvasJSize = canvasCellSize*width;
  this.resize(canvasISize, canvasJSize);
  this.clear();
  ctx.beginPath();
  ctx.strokeStyle = 'black';
  ctx.fillStyle = '#bfbfbf';

  // ** Add stuff you want drawn in the background all the time here **
  ctx.lineWidth = 2;
  for (let i = 0; i < height; i++) {
    for (let j = (i+1)%2; j < width; j+=2) {
      let x = canvasOffset + canvasCellSize*j;
      let y = canvasOffset + canvasCellSize*i;
      ctx.fillRect(x, y, canvasCellSize, canvasCellSize);
    }
  }
  ctx.strokeRect(canvasOffset,canvasOffset,canvasJSize,canvasISize);

  // for (let i = 1; i < width; i++) {
  //   ctx.moveTo(canvasOffset+i*(xPos(1, width)-xPos(0, width)), canvasOffset);
  //   ctx.lineTo(canvasOffset+i*(xPos(1, width)-xPos(0, width)), canvasOffset+canvasSize);
  // }
  // for (let i = 1; i < height; i++) {
  //   ctx.moveTo(canvasOffset, canvasOffset+i*(yPos(1, height)-yPos(0, height)));
  //   ctx.lineTo(canvasOffset+canvasSize, canvasOffset+i*(yPos(1, height)-yPos(0, height)));
  // }
  // ctx.stroke();


  ctx.fillStyle = 'black';
  ctx.lineWidth = 1;
  // draw all cells
  for (let i = 0; i < height; i++) {
    for (let j = 0; j < width; j++) {
      //draw vertex
      ctx.beginPath();
      let nodeRadius = 2;
      ctx.arc(xPos(j, width, canvasJSize), yPos(i, height, canvasISize), nodeRadius, 0, Math.PI * 2, true);
      ctx.fill();

      let moves = tour[i][j];
      let i1 = i+movesI[moves[0]];
      let j1 = j+movesJ[moves[0]];
      let i2 = i+movesI[moves[1]];
      let j2 = j+movesJ[moves[1]];
      // console.log(i,j,tour[i][j],moves,i1,j1,i2,j2);
      ctx.beginPath();
      ctx.moveTo(xPos(j, width, canvasJSize), yPos(i, height, canvasISize));
      ctx.lineTo(xPos(j1, width, canvasJSize), yPos(i1, height, canvasISize));
      ctx.moveTo(xPos(j, width, canvasJSize), yPos(i, height, canvasISize));
      ctx.lineTo(xPos(j2, width, canvasJSize), yPos(i2, height, canvasISize));
      ctx.stroke();
    }
  }

  // ** Add stuff you want drawn on top all the time here **
  this.valid = true;
}

////////////////////////////////////
//HTML interaction
////////////////////////////////////

var CS = new CanvasState(document.getElementById('canvas1'));
init();

function init() {
  CS.valid = false;
  let tour = genTour(30, 30);
  setTurnCount(numTurns(tour),tour.length);
  setCrossingCount(numCrossings(tour),tour.length);
}

//Algorithm 1 in the paper
function genTour(width, height) {
  if (width < 16 || width % 2 != 0 || height < 12) {
    alert("width should be >=16 and even. height should be >=12");
    return;
  }

  let BRSeq = (width/2+2)%4; //bottom-right corner Sequence
  let TLSeq = (((3-height)%4)+4)%4; //top-left corner Sequence
  let TRHeight = 5+((width/2+height-1)%4); //top-right corner junction height

  let tour = emptyTour(width, height);

  //Left side
  let i = height-7;
  while (i >= 0) {
    addPiece(tour, i, 0, VerticalEdge);
    i -= 4;
  }
  //Right side
  switch(BRSeq) {
    case 0: i = height - 8;
      break;
    case 1: i = height - 7;
      break;
    case 2: i = height - 10;
      break;
    case 3: i = height - 9;
      break;
    default: alert("bug");
  }
  while (i >= 0) {
    addPiece(tour, i, width-2, rotate180(VerticalEdge));
    i -= 4;
  }
  //Bottom Side
  addPiece(tour, height-5, 0, CornerHMatchHeight5);
  let j = 6;
  let finalj;
  switch(BRSeq) {
    case 0: finalj = width - 6;
      break;
    case 1: finalj = width - 8;
      break;
    case 2: finalj = width - 10;
      break;
    case 3: finalj = width - 4;
      break;
    default: alert("bug");
  }
  while (j < finalj) {
    addPiece(tour, height-4, j, Sequence1);
    j += 8;
  }
  switch(BRSeq) {
    case 0: addPiece(tour, height-4, j, Sequence0);
      break;
    case 1: addPiece(tour, height-4, j, Sequence1);
      break;
    case 2:
      addPiece(tour, height-4, j, Sequence0);
      addPiece(tour, height-6, j+6, Sequence2part2);
      break;
    case 3: addPiece(tour, height-5, j, Sequence3);
      break;
    default: alert("bug");
  }
  // Top Side
  switch(TLSeq) {
    case 0:
      addPiece(tour, 0, 0, rotate180(Sequence0));
      j = 6;
      break;
    case 1:
      addPiece(tour, 0, 0, rotate180(Sequence1));
      j = 8;
      break;
    case 2:
      addPiece(tour, 0, 0, rotate180(Sequence2part2));
      addPiece(tour, 0, 4, rotate180(Sequence0));
      j = 10;
      break;
    case 3:
      addPiece(tour, 0, 0, rotate180(Sequence3));
      j = 4;
      break;
    default: alert("bug");
  }
  while (j < width-8) {
    addPiece(tour, 0, j, rotate180(Sequence1));
    j += 8;
  }
  switch(TRHeight) {
    case 5: addPiece(tour, 0, width-6, rotate180(CornerVMatchHeight5));
      break;
    case 6: addPiece(tour, 0, width-8, rotate180(CornerVMatchHeight6));
      break;
    case 7: addPiece(tour, 0, width-10, rotate180(CornerVMatchHeight7));
      break;
    case 8: addPiece(tour, 0, width-12, rotate180(CornerVMatchHeight8));
      break;
    default: alert("bug");
  }

  return tour;
}

function flipCell(cell) {
  if (cell == 'xx') return 'xx';
  res = [0,0];
  for (let i = 0; i < 2; i++) {
    res[i] = ((parseInt(cell[i])+4)%8).toString();
  }
  return res.join("");
}

//messy because of the format of the structures
//and the required conversions strings->arrays->strings
function rotate180(struct) {
  let height = struct.length;
  let lineArrays = [];
  for (let i = 0; i < height; i++) {
    lineArrays[i] = struct[height-1-i].split(' ');
  }
  let width = lineArrays[0].length;
  let res = [];
  for (let i = 0; i < height; i++) {
    res[i] = new Array(width);
  }
  for (let i = 0; i < height; i++) {
    for (let j = 0; j < width; j++) {
      res[i][j] = flipCell(lineArrays[i][width-1-j]);
    }
  }
  for (let i = 0; i < height; i++) {
    res[i] = res[i].join(' ');
  }
  return res;
}

function addPiece(tour, istart, jstart, struct) {
  for (let i = 0; i < struct.length; i++) {
    let line = struct[i].split(" ");
    for (let j = 0; j < line.length; j++) {
      if (line[j] != 'xx') tour[istart+i][jstart+j] = line[j];
    }
  }
}

function emptyTour(width, height) {
  // Everything begins as a northWest-southEast diagonal
  var tour = [];
  for (let i = 0; i < height; ++i) {
    tour[i] = [];
    for (let j = 0; j < width; ++j) {
      tour[i][j] = '26';
    }
  }
  return tour;
}

function changeBoardSize() {

  let width = parseInt(document.getElementById('newwidth').value);
  let height = parseInt(document.getElementById('newheight').value);
  console.log("Generating tour for width = " + width + " height = " + height);
  let tour = genTour(width, height);
  if (tour === undefined) return;
  if (validateTour(tour)) {
    console.log("Validated tour");
    CS.tour = tour;
    CS.valid = false;
    setTurnCount(numTurns(tour),tour.length);
    setCrossingCount(numCrossings(tour),tour.length);
  }
  else {
    CS.tour = tour;
    CS.valid = false;
    alert('incorrect tour');
  }
}

function numTurns(tour) {
  let isize = tour.length;
  let jsize = tour[0].length;
  let count = 0;
  for (let i = 0; i < isize; i++) {
    for (let j = 0; j < jsize; j++) {
      count++;//add one, and subtract it back if its not a turn
      if (tour[i][j] === '04' || tour[i][j] === '15' || tour[i][j] === '26' || tour[i][j] === '37') {
        count--;
      }
    }
  }
  return count;
}

function orientation(px,py,qx,qy,rx,ry) {
    let val = (qy-py)*(rx-qx)-(qx-px)*(ry-qy);
    if (val == 0) return 0;  // colinear
    return (val > 0)? 1: 2; // clock or counterclock wise
}
//returns whether the OPEN segments (p1,p2) and
//(q1,q2) intersect
//bug: if the segments share an endpoint it returns true
function isACrossing(p1x,p1y,p2x,p2y,q1x,q1y,q2x,q2y) {
  let o1 = orientation(p1x,p1y,p2x,p2y,q1x,q1y);
  let o2 = orientation(p1x,p1y,p2x,p2y,q2x,q2y);
  let o3 = orientation(q1x,q1y,q2x,q2y,p1x,p1y);
  let o4 = orientation(q1x,q1y,q2x,q2y,p2x,p2y);
  return (o1 != 0 && o2 != 0 && o3 != 0 && o4 != 0 && o1 != o2 && o3 != o4);
}

function numCrossings(tour) {
  let isize = tour.length;
  let jsize = tour[0].length;
  let count = 0; //init crossing count to 0
  //for each cell C
  for (let i = 0; i < isize; i++) {
    for (let j = 0; j < jsize; j++) {
      //for each nearby cell C'
      for (let i2 = i-3; i2 <= i+3; i2++) {
        for (let j2 = j-3; j2 <= j+3; j2++) {
          //check that its not out of bounds
          if (i2 >= 0 && i2 < isize && j2 >= 0 && j2 < jsize) {
            //for each of the two moves involving C
            for (let k = 0; k < 2; k++) {
              //for each of the two moves involving C'
              for (let k2 = 0; k2 < 2; k2++) {
                //initialize the 4 endpionts of the segment moves
                //(it doesnt matter that it is flipping the coordinate system)
                let p1x=i, p1y=j, q1x=i2, q1y=j2;
                let p2x = i+movesI[tour[i][j][k]];
                let p2y = j+movesJ[tour[i][j][k]];
                let q2x = i2+movesI[tour[i2][j2][k2]];
                let q2y = j2+movesJ[tour[i2][j2][k2]];
                //skip check if the 2 segments share an endpoint (cannot be Xing)
                if ((p1x == q1x && p1y == q1y) || (p1x == q2x && p1y == q2y) ||
                    (p2x == q1x && p2y == q1y) || (p2x == q2x && p2y == q2y)) {
                  continue;
                } else {
                  if (isACrossing(p1x,p1y,p2x,p2y,q1x,q1y,q2x,q2y)) {
                    count++;
                    // console.log(p1x,p1y,p2x,p2y,q1x,q1y,q2x,q2y);
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  return count/8; //each crossing is counted twice from each endpoint of each move
}

// Tour given as an array of array of strings
// Returns true if the tour is a valid tour for the board.
function validateTour(tour) {
  let n = tour.length;
  let m = tour[0].length;
  let squares = []
  for (let i = 0; i < n; i++) {
    squares[i] = [];
    for (let j = 0; j < m; j++) {
      squares[i][j] = false;
    }
  }

  let prevRow = 0, prevColumn = 0;
  let row = 0, column = 0, steps = 0;
  while (steps < n * m) {
    // Since we don't know which move goes forward and which goes backward, we store
    // the previous location and try both.
    let nextMove = parseInt(tour[row][column]) % 10;
    let newRow = row + movesI[nextMove];
    let newColumn = column + movesJ[nextMove];
    // If the first move takes us to the previous location, try the second one.
    if (newRow == prevRow && newColumn == prevColumn) {
      nextMove = Math.trunc(parseInt(tour[row][column]) / 10);
      newRow = row + movesI[nextMove];
      newColumn = column + movesJ[nextMove];
    }
    // If steps == 0, then we don't have a previous location. But otherwise,
    // if the first move takes us to a new location, check that the second move
    // takes us back to the previous location.
    else if (steps > 0) {
      prevMove = Math.trunc(parseInt(tour[row][column]) / 10);
      checkPrevRow = row + movesI[prevMove];
      checkPrevColumn = column + movesJ[prevMove];
      if (checkPrevRow != prevRow || checkPrevColumn != prevColumn) {
        console.log("neither moves takes us back to a prevoius location",row,column,newRow,newColumn);
        return false;
      }
    }

    if (newRow < 0 || newRow > n || newColumn < 0 || newColumn > m) {
      console.log("tour goes out of bounds");
      return false;
    }
    else if (squares[newRow][newColumn]) {
      console.log("cell was already visited " + newRow + "," + newColumn);
      return false;
    }

    squares[newRow][newColumn] = true;
    prevRow = row, prevColumn = column;
    row = newRow, column = newColumn;
    steps++;
  }
  return true;
}

function round(value, decimals) {
  return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
}

//only works for square matrices for now
function setTurnCount(numTurns,boardSize) {
  document.getElementById('turncount').innerHTML =
    'Number of turns: '.concat(numTurns);
}

//only works for square matrices for now
function setCrossingCount(numCrossings,boardSize) {
  document.getElementById('crossingcount').innerHTML =
    'Number of crossings: '.concat(numCrossings);
}



