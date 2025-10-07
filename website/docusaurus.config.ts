import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Xenon Space',
  tagline: 'Jeu de stratégie spatiale en Python',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  // Remplacez par votre nom d'utilisateur GitHub
  url: 'https://nonov1012.github.io',
  baseUrl: '/xenon-space---Video-game/',

  // Configuration GitHub pages
  organizationName: 'nonov1012', // Votre nom d'utilisateur GitHub
  projectName: 'xenon-space---Video-game', // Nom de votre repo

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'fr',
    locales: ['fr', 'en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/nonov1012/xenon-space---Video-game/tree/main/website/',
        },
        blog: false, // Désactiver le blog si non utilisé
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/xenon-space-social-card.jpg',
    colorMode: {
      defaultMode: 'dark',
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Xenon Space',
      logo: {
        alt: 'Xenon Space Logo',
        src: 'img/logo.png',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: '📚 Documentation',
        },
        {
          type: 'localeDropdown',
          position: 'right',
        },
        {
          href: 'https://github.com/nonov1012/xenon-space---Video-game',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
            {
              label: 'Guide Technique',
              to: '/docs/technical/intro',
            },
            {
              label: 'Guide Utilisateur',
              to: '/docs/users/intro',
            },
          ],
        },
        {
          title: 'Équipe',
          items: [
            {
              label: 'VOITURIER Noa',
              href: '#',
            },
            {
              label: 'NOËL Clément',
              href: '#',
            },
            {
              label: 'DAVID Gabriel',
              href: '#',
            },
            {
              label: 'DUPUIS Brian',
              href: '#',
            },
            {
              label: 'CAVEL Ugo',
              href: '#',
            },
            {
              label: 'VANHOVE Tom',
              href: '#',
            },
          ],
        },
        {
          title: 'Liens',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/nonov1012/xenon-space---Video-game',
            },
            {
              label: 'Issues',
              href: 'https://github.com/nonov1012/xenon-space---Video-game/issues',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Xenon Space Team. Construit avec Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;