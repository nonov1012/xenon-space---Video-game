import type { JSX } from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';
import React from 'react';

import StarsBackground from '@site/src/components/SpaceBackground/StarsBackground';
import SpaceObjects from '@site/src/components/SpaceBackground/SpaceObjects';

import styles from './index.module.css';

function HomepageHeader(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={styles.heroBanner}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>

        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/technicals/intro"
          >
            📘 Documentation Technique
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/docs/users/intro"
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
      {/* Fond spatial derrière le header */}
      <div className={styles.spaceBackground}>
        <StarsBackground />
        <SpaceObjects />
      </div>

      {/* Header transparent par-dessus */}
      <HomepageHeader />

      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
