import React, { useRef, useEffect, useState } from 'react';

interface Star {
  x: number;
  y: number;
  r: number;
  baseColor: [number, number, number];
  phase: number;
  speed: number;
}

export default function SpaceBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [canvasWidth, setCanvasWidth] = useState(window.innerWidth);
  const stars = useRef<Star[]>([]);
  const angle = useRef(0);

  // Initialisation
  useEffect(() => {
    // Étoiles
    stars.current = [];
    for (let i = 0; i < 150; i++) {
      stars.current.push({
        x: Math.random() * canvasWidth,
        y: Math.random() * 400,
        r: Math.random() * 2 + 1,
        baseColor: [
          [255, 255, 255],
          [200, 200, 255],
          [255, 255, 180],
        ][Math.floor(Math.random() * 3)] as [number, number, number],
        phase: Math.random() * Math.PI * 2,
        speed: 0.05,
      });
    }
  }, [canvasWidth]);

  // Redimensionnement
  useEffect(() => {
    const handleResize = () => setCanvasWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Boucle d'animation du canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationId: number;

    const animate = () => {
      // Fond noir
      ctx.fillStyle = 'black';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      angle.current += 0.01; // clignotement doux

      // Étoiles
      stars.current.forEach((s) => {
        s.x = (s.x + s.speed) % canvas.width;
        const brightness = 200 + 55 * Math.sin(angle.current + s.phase);
        const f = brightness / 255;
        const [r, g, b] = s.baseColor.map((c) => Math.floor(c * f));

        ctx.fillStyle = `rgb(${r},${g},${b})`;
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fill();
      });

      animationId = requestAnimationFrame(animate);
    };

    animate();
    return () => cancelAnimationFrame(animationId);
  }, []);

  return (
    <div style={{ position: 'relative', width: '100%', height: '400px', overflow: 'hidden' }}>
      <canvas
        ref={canvasRef}
        width={canvasWidth}
        height={400}
        style={{ display: 'block', width: '100%', height: '400px' }}
      />
    </div>
  );
}
