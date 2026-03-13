import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  emoji: string;
  description: ReactNode;
  link: string;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Framework de Agentes',
    emoji: '🤖',
    description: (
      <>
        Aprende a criar equipas de agentes de IA com o <strong>CrewAI</strong>.
        Cada agente é especialista numa tarefa e colabora com os outros para
        resolver problemas complexos.
      </>
    ),
    link: '/docs/intro',
  },
  {
    title: 'Projecto AI Investor',
    emoji: '📈',
    description: (
      <>
        Um sistema completo de análise financeira com 4 agentes: investigação
        de notícias, análise técnica (RSI/SMA), estratégia de investimento e
        geração de relatórios em PDF.
      </>
    ),
    link: '/docs/ai-investor/overview',
  },
  {
    title: 'Docker & Produção',
    emoji: '🐳',
    description: (
      <>
        Containeriza o teu sistema multi-agente com <strong>Docker</strong> e{' '}
        <strong>Docker Compose</strong> para deployment reprodutível em qualquer
        ambiente, com suporte a múltiplos fornecedores de LLM.
      </>
    ),
    link: '/docs/ai-investor/docker',
  },
];

function Feature({title, emoji, description, link}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <div className={styles.featureEmoji} role="img" aria-label={title}>
          {emoji}
        </div>
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
        <Link className="button button--primary button--sm" to={link}>
          Saber mais →
        </Link>
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
      </div>
    </section>
  );
}
