import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'minicloud Agent',
  tagline: 'LangGraph ReAct research agent — OpenAI-compatible AI service',
  favicon: 'img/favicon.ico',
  url: 'https://andrelair-platform.github.io',
  baseUrl: '/minicloud-agent/',
  organizationName: 'andrelair-platform',
  projectName: 'minicloud-agent',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  i18n: {defaultLocale: 'en', locales: ['en']},
  markdown: {mermaid: true},
  themes: ['@docusaurus/theme-mermaid'],
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: '/',
        },
        blog: false,
        theme: {customCss: './src/css/custom.css'},
      } satisfies Preset.Options,
    ],
  ],
  themeConfig: {
    navbar: {
      title: 'minicloud-agent',
      items: [
        {href: 'https://andrelair-platform.github.io/minicloud-platform-docs/', label: 'Platform docs', position: 'right'},
        {href: 'https://github.com/andrelair-platform/minicloud-agent', label: 'GitHub', position: 'right'},
      ],
    },
    prism: {
      additionalLanguages: ['python', 'bash', 'yaml', 'json'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
