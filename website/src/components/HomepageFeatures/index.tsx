import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  img: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'But du jeu',
    img: require('@site/static/img/base.png').default,
    description: (
      <>
        Xenon Space est un Jeu de stratégie spatiale en 1vs1, tour par tour.
        Votre but est de détruire la base de votre adversaire en protégeant la
        vôtre.
      </>
    ),
  },
  {
    title: 'De nombreux vaisseaux',
    img: require('@site/static/img/vaisseau.png').default,
    description: (
      <>
        De nombreux vaisseaux seront à votre disposition pour atteindre votre objectif : 
        certains font plus de dégâts, d’autres se déplacent plus rapidement, et d’autres encore génèrent de l’argent.
        À vous de faire les bons choix !
      </>
    ),
  },
  {
    title: 'Des planètes variées',
    img: require('@site/static/img/planete.gif').default,
    description: (
      <>
        De nombreuses planètes et astéroïdes sont disséminés dans l’espace.
        Elles vous permettront de gagner plus d’argent.
        À vous de les exploiter !
      </>
    ),
  },
];

function Feature({ title, img, description }: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <img src={img} alt={title} className={styles.featureImg} />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>

        {/* 🎬 Section YouTube Trailer */}
        <div className="text--center margin-top--xl">
          <Heading as="h3">Découvrez Xenon Space en vidéo</Heading>
          <div className={styles.videoContainer}>
            <iframe
              width="800"
              height="450"
              src="https://www.youtube.com/embed/o76fH_eu0nM"  // 🔁 Remplace par ton ID YouTube
              title="Xenon Space Official Trailer"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            ></iframe>
          </div>
        </div>
      </div>
    </section>
  );
}
