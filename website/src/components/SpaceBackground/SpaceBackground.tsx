// src/components/SpaceBackground.tsx
import React from 'react';
import StarsBackground from '@site/src/components/SpaceBackground/StarsBackground';
import SpaceObjects from '@site/src/components/SpaceBackground/SpaceObjects';

export default function SpaceBackground() {
  return (
    <div style={{ position: 'relative', width: '100%', height: 400 }}>
      <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' }}>
        <StarsBackground />
      </div>
      <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' }}>
        <SpaceObjects />
      </div>
    </div>
  );
}
