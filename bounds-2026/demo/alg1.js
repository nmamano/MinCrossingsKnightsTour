// Algorithm 1 of the paper (Besa, Johnson, Mamano, Osegueda 2019): the generator of the 2019 demo (board.js),
// moved here unchanged except for the wrapper. Rectangular boards: width even >= 16, height >= 12.
(function (root) {
  'use strict';
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


//Algorithm 1 in the paper
function genTour(width, height) {
  if (width < 16 || width % 2 != 0 || height < 12) {
    return null;
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
    default: throw new Error("bug");
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
    default: throw new Error("bug");
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
    default: throw new Error("bug");
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
    default: throw new Error("bug");
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
    default: throw new Error("bug");
  }

  return tour;
}

function flipCell(cell) {
  if (cell == 'xx') return 'xx';
  const res = [0,0];
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

  const ALG1 = { genTour };
  if (typeof module !== 'undefined') module.exports = ALG1; else root.ALG1 = ALG1;
})(this);
