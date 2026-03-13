import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'CrewAI Book',
  tagline: 'Guia Prático – Multi-Agentes com CrewAI + Docker',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://icpmtech.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/CrewAIBook/',

  // GitHub pages deployment config.
  organizationName: 'icpmtech',
  projectName: 'CrewAIBook',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'pt',
    locales: ['pt', 'en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/icpmtech/CrewAIBook/tree/main/website/',
          routeBasePath: 'docs',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          editUrl: 'https://github.com/icpmtech/CrewAIBook/tree/main/website/',
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/crewai-social-card.png',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'CrewAI Book',
      logo: {
        alt: 'CrewAI Book Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'guideSidebar',
          position: 'left',
          label: 'Guia',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {
          href: 'https://github.com/icpmtech/CrewAIBook',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentação',
          items: [
            {
              label: 'Introdução',
              to: '/docs/intro',
            },
            {
              label: 'Instalação',
              to: '/docs/installation',
            },
            {
              label: 'Projeto AI Investor',
              to: '/docs/ai-investor/overview',
            },
          ],
        },
        {
          title: 'Recursos',
          items: [
            {
              label: 'CrewAI Oficial',
              href: 'https://docs.crewai.com',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/icpmtech/CrewAIBook',
            },
          ],
        },
        {
          title: 'Mais',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} CrewAI Book. Construído com Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'docker', 'yaml'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
