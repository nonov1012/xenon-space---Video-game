import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/xenon-space---Video-game/__docusaurus/debug',
    component: ComponentCreator('/xenon-space---Video-game/__docusaurus/debug', 'b17'),
    exact: true
  },
  {
    path: '/xenon-space---Video-game/__docusaurus/debug/config',
    component: ComponentCreator('/xenon-space---Video-game/__docusaurus/debug/config', '64b'),
    exact: true
  },
  {
    path: '/xenon-space---Video-game/__docusaurus/debug/content',
    component: ComponentCreator('/xenon-space---Video-game/__docusaurus/debug/content', '777'),
    exact: true
  },
  {
    path: '/xenon-space---Video-game/__docusaurus/debug/globalData',
    component: ComponentCreator('/xenon-space---Video-game/__docusaurus/debug/globalData', '7fd'),
    exact: true
  },
  {
    path: '/xenon-space---Video-game/__docusaurus/debug/metadata',
    component: ComponentCreator('/xenon-space---Video-game/__docusaurus/debug/metadata', 'd00'),
    exact: true
  },
  {
    path: '/xenon-space---Video-game/__docusaurus/debug/registry',
    component: ComponentCreator('/xenon-space---Video-game/__docusaurus/debug/registry', '320'),
    exact: true
  },
  {
    path: '/xenon-space---Video-game/__docusaurus/debug/routes',
    component: ComponentCreator('/xenon-space---Video-game/__docusaurus/debug/routes', '273'),
    exact: true
  },
  {
    path: '/xenon-space---Video-game/markdown-page',
    component: ComponentCreator('/xenon-space---Video-game/markdown-page', 'c4d'),
    exact: true
  },
  {
    path: '/xenon-space---Video-game/docs',
    component: ComponentCreator('/xenon-space---Video-game/docs', '211'),
    routes: [
      {
        path: '/xenon-space---Video-game/docs',
        component: ComponentCreator('/xenon-space---Video-game/docs', '97f'),
        routes: [
          {
            path: '/xenon-space---Video-game/docs',
            component: ComponentCreator('/xenon-space---Video-game/docs', '10d'),
            routes: [
              {
                path: '/xenon-space---Video-game/docs/intro',
                component: ComponentCreator('/xenon-space---Video-game/docs/intro', '821'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/xenon-space---Video-game/docs/technicals/architecture',
                component: ComponentCreator('/xenon-space---Video-game/docs/technicals/architecture', '16b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/xenon-space---Video-game/docs/technicals/intro',
                component: ComponentCreator('/xenon-space---Video-game/docs/technicals/intro', '70e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/xenon-space---Video-game/docs/technicals/requirements',
                component: ComponentCreator('/xenon-space---Video-game/docs/technicals/requirements', '1b5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/xenon-space---Video-game/docs/users/gameplay',
                component: ComponentCreator('/xenon-space---Video-game/docs/users/gameplay', 'cc2'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/xenon-space---Video-game/docs/users/installation',
                component: ComponentCreator('/xenon-space---Video-game/docs/users/installation', 'df7'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/xenon-space---Video-game/docs/users/intro',
                component: ComponentCreator('/xenon-space---Video-game/docs/users/intro', '4c5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/xenon-space---Video-game/docs/users/mechanics',
                component: ComponentCreator('/xenon-space---Video-game/docs/users/mechanics', '3ff'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/xenon-space---Video-game/docs/users/menu/fin',
                component: ComponentCreator('/xenon-space---Video-game/docs/users/menu/fin', '637'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/xenon-space---Video-game/docs/users/menu/jouer',
                component: ComponentCreator('/xenon-space---Video-game/docs/users/menu/jouer', '3f4'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/xenon-space---Video-game/docs/users/menu/parametre',
                component: ComponentCreator('/xenon-space---Video-game/docs/users/menu/parametre', '9c4'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/xenon-space---Video-game/docs/users/menu/pause',
                component: ComponentCreator('/xenon-space---Video-game/docs/users/menu/pause', 'cff'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/xenon-space---Video-game/docs/users/menu/succes',
                component: ComponentCreator('/xenon-space---Video-game/docs/users/menu/succes', 'c86'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/xenon-space---Video-game/docs/users/tutoriel',
                component: ComponentCreator('/xenon-space---Video-game/docs/users/tutoriel', '5ea'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/xenon-space---Video-game/',
    component: ComponentCreator('/xenon-space---Video-game/', 'c2d'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
