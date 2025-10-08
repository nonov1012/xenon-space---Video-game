import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: '🔧 Documentation Technique',
      items: [
        'technicals/intro',
        'technicals/requirements',
      ],
    },
    {
      type: 'category',
      label: '👤 Documentation Utilisateur',
      items: [
        'users/intro',
        'users/presentation',
        'users/interface',
        'users/installation',
        'users/gameplay',
        'users/strategies',
        'users/vaisseaux',
      ],
    },
  ],
};

export default sidebars;