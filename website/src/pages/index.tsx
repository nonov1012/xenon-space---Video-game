import type { JSX } from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';
import React from 'react';

import StarsBackground from '@site/src/components/SpaceBackground/StarsBackground';

import styles from './index.module.css';
import BrowserOnly from '@docusaurus/BrowserOnly';

function HomepageHeader(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={styles.heroBanner}>
      <div className="container" style={{ color: 'white'}}>
        <Heading as="h1" className={`hero__title ${styles.responsiveTitle}`}>
          {siteConfig.title}
        </Heading>
        <p className={`hero__subtitle ${styles.responsiveSubtitle}`}>{siteConfig.tagline}</p>

        <div
          className={styles.buttons}
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'center',
            gap: 'clamp(0.5rem, 2vw, 1.5rem)',
          }}
        >
          <Link
            className="button button--secondary button--lg"
            to="/docs/technicals/intro"
            style={{
              fontSize: 'clamp(0.875rem, 2vw, 1.125rem)',
              padding: 'clamp(0.5rem, 1vw, 0.75rem) clamp(1rem, 2vw, 1.5rem)',
            }}
          >
            📘 Documentation Technique
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/docs/users/intro"
            style={{
              fontSize: 'clamp(0.875rem, 2vw, 1.125rem)',
              padding: 'clamp(0.5rem, 1vw, 0.75rem) clamp(1rem, 2vw, 1.5rem)',
            }}
          >
            🧭 Documentation Utilisateur
          </Link>
        </div>

      </div>
    </header>
  );
}

export default function Home(): JSX.Element {
  return (
    <Layout title="Accueil" description="Description du site">
      <BrowserOnly>
        {/* Fond spatial derrière le header */}
        {() => (
          <div className={styles.spaceBackground}>
            <StarsBackground />
          </div>
        )}
      </BrowserOnly>

      {/* Header transparent par-dessus */}
      <HomepageHeader />

      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}