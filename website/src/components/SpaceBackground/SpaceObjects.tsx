// src/components/SpaceObjects.tsx
import React from 'react';
import Sketch from 'react-p5';

interface Sprite {
  img: any;
  x: number;
  y: number;
  w: number;
  h: number;
  speed: number;
}

let ship: Sprite;
let planets: Sprite[] = [];

export default function SpaceObjects() {
  const preload = (p5: any) => {
    // Vaisseau (image statique pour l'instant)
    ship = {
      img: p5.loadImage('/img/base.png'), // mettre dans static/img/
      x: 0,
      y: 0,
      w: 160,
      h: 200,
      speed: 0
    };

    // Planètes avec positions et vitesses différentes
    planets.push({ img: p5.loadImage('/img/planet1.png'), x: -50, y: 50, w: 60, h: 60, speed: 0.5 });
    planets.push({ img: p5.loadImage('/img/planet2.png'), x: -150, y: 150, w: 80, h: 80, speed: 1 });
    planets.push({ img: p5.loadImage('/img/planet3.png'), x: -300, y: 100, w: 40, h: 40, speed: 0.3 });
  };

  const setup = (p5: any, canvasParentRef: any) => {
    p5.createCanvas(p5.windowWidth, 400).parent(canvasParentRef);

    // Position initiale du vaisseau
    ship.x = p5.width / 2;
    ship.y = 300;
  };

  const draw = (p5: any) => {
    // Planètes qui défilent
    planets.forEach(p => {
      p.x += p.speed;

      // Si la planète sort de l'écran à droite, elle revient à gauche
      if (p.x > p5.width + p.w) {
        p.x = -p.w;
        p.y = Math.random() * (p5.height - p.h) + p.h / 2;
      }

      p5.imageMode(p5.CENTER);
      p5.image(p.img, p.x, p.y, p.w, p.h);
    });

    // Vaisseau
    p5.imageMode(p5.CENTER);
    p5.image(ship.img, ship.x, ship.y, ship.w, ship.h);
  };

  const windowResized = (p5: any) => {
    p5.resizeCanvas(p5.windowWidth, 400);
  };

  return <Sketch preload={preload} setup={setup} draw={draw} windowResized={windowResized} />;
}
