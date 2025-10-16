import React from 'react';
import Sketch from 'react-p5';

interface Star {
  x: number;
  y: number;
  r: number;
  baseColor: [number, number, number];
  phase: number;
}

let stars: Star[] = [];
let angle = 0;

export default function SpaceBackground() {
  const setup = (p5: any, canvasParentRef: any) => {
    p5.createCanvas(p5.windowWidth, 400).parent(canvasParentRef);

    // Créer des étoiles aléatoires
    for (let i = 0; i < 150; i++) {
      stars.push({
        x: Math.random() * p5.width,
        y: Math.random() * p5.height,
        r: Math.random() * 3 + 1,
        baseColor: [[255,255,255],[200,200,255],[255,255,180]][Math.floor(Math.random()*3)] as [number, number, number],
        phase: Math.random() * p5.TWO_PI
      });
    }
  };

  const draw = (p5: any) => {
    p5.background(0);
    angle += 0.05;

    // Dessiner les étoiles avec scintillement, sans bouger verticalement
    for (let s of stars) {
      s.x = (s.x + 1) % p5.width;
      const brightness = 200 + 55 * Math.sin(angle + s.phase);
      const f = brightness / 255;
      const c = p5.color(s.baseColor[0]*f, s.baseColor[1]*f, s.baseColor[2]*f);
      p5.noStroke();
      p5.fill(c);
      p5.circle(s.x, s.y, s.r);
    }
  };

  const windowResized = (p5: any) => {
    p5.resizeCanvas(p5.windowWidth, 400);
  };

  return <Sketch setup={setup} draw={draw} windowResized={windowResized} />;
}
