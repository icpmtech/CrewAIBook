import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  guideSidebar: [
    'intro',
    'installation',
    'project-structure',
    {
      type: 'category',
      label: 'Projeto AI Investor',
      items: [
        'ai-investor/overview',
        'ai-investor/tools',
        'ai-investor/main',
        'ai-investor/docker',
        'ai-investor/environment',
        'ai-investor/pdf-export',
        'ai-investor/running',
      ],
    },
    'architecture',
    'advanced',
  ],
};

export default sidebars;
