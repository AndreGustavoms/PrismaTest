/**
 * Conteúdo da landing page do Prisma.
 * Texto separado da apresentação: edite a copy aqui, sem tocar em JSX.
 */

export const marca = {
  nome: 'Prisma',
  descricao:
    'Plataforma de estudos com IA para instituições de ensino: um crédito, três perfis, memória que acompanha o aluno.',
}

export const navegacao = [
  { rotulo: 'Como funciona', href: '#como-funciona' },
  { rotulo: 'Perfis', href: '#perfis' },
  { rotulo: 'Recursos', href: '#recursos' },
  { rotulo: 'Créditos', href: '#creditos' },
]

export const hero = {
  etiqueta: 'IA aplicada ao ensino',
  titulo: 'Uma entrada. Todo o espectro do ensino.',
  subtitulo:
    'Um tema entra. Saem materiais prontos para aluno, professor e diretor.',
  ctaPrimario: 'Começar agora',
  ctaSecundario: 'Ver como funciona',
  apoio: 'Sem cartão de crédito.',
}

/**
 * Exemplos do demo do motor de refração.
 *
 * Cada saída declara para QUEM ela serve. É isso que define a cor
 * exibida — a cor identifica o perfil destinatário, não a posição
 * na lista (ver "REGRA DE COR" em index.css).
 */
export const exemplosRefracao = [
  {
    entrada: 'Fotossíntese — 7º ano',
    saidas: [
      { rotulo: 'Resumo guiado', perfil: 'aluno' },
      { rotulo: 'Quiz de 10 questões', perfil: 'aluno' },
      { rotulo: 'Plano de aula', perfil: 'professor' },
    ],
  },
  {
    entrada: 'Revolução Francesa — Ensino Médio',
    saidas: [
      { rotulo: 'Linha do tempo', perfil: 'aluno' },
      { rotulo: 'Prova dissertativa', perfil: 'professor' },
      { rotulo: 'Relatório da turma', perfil: 'diretor' },
    ],
  },
  {
    entrada: 'Frações — 5º ano',
    saidas: [
      { rotulo: 'Lista progressiva', perfil: 'aluno' },
      { rotulo: 'Exercícios resolvidos', perfil: 'aluno' },
      { rotulo: 'Diagnóstico da turma', perfil: 'professor' },
    ],
  },
  {
    entrada: 'Ciclo da água — 4º ano',
    saidas: [
      { rotulo: 'Mapa visual', perfil: 'aluno' },
      { rotulo: 'Roteiro de aula', perfil: 'professor' },
      { rotulo: 'Indicador de engajamento', perfil: 'diretor' },
    ],
  },
] as const

export const perfis = [
  {
    id: 'aluno',
    nome: 'Aluno',
    foco: 'Estudar com apoio contínuo',
    corVar: 'var(--color-aluno)',
    tintVar: 'var(--color-lavender-tint)',
    itens: [
      'Tutor que lembra o que você já estudou',
      'Simulados com correção comentada',
      'Notas e faltas em um só lugar',
    ],
  },
  {
    id: 'professor',
    nome: 'Professor',
    foco: 'Ensinar sem o trabalho repetitivo',
    corVar: 'var(--color-professor)',
    tintVar: 'var(--color-terracotta-tint)',
    itens: [
      'Provas geradas a partir do seu conteúdo',
      'Correção assistida, sempre com sua revisão',
      'Banco de material reutilizável',
    ],
  },
  {
    id: 'diretor',
    nome: 'Diretor',
    foco: 'Administrar com visibilidade real',
    corVar: 'var(--color-diretor)',
    tintVar: 'var(--color-olive-tint)',
    itens: [
      'Desempenho por turma em painel',
      'Distribuição de créditos entre perfis',
      'Consumo de IA auditável',
    ],
  },
]

/**
 * Quatro recursos, não seis: a landing vende o essencial.
 * O restante (chave protegida, painel por turma) entra na página
 * de produto, quando existir.
 */
export const recursos = [
  {
    titulo: 'Motor multi-modelo',
    descricao: 'Cada tarefa vai para o modelo mais adequado em custo.',
  },
  {
    titulo: 'Memória persistente',
    descricao: 'O tutor retoma o contexto do aluno sem reler tudo.',
  },
  {
    titulo: 'Créditos auditáveis',
    descricao: 'Débito só depois de uma resposta entregue.',
  },
  {
    titulo: 'Revisão do professor',
    descricao: 'Conteúdo de IA nasce rascunho. Quem ensina aprova.',
  },
]

export const creditos = {
  etiqueta: 'Créditos',
  titulo: 'A instituição assina. O diretor distribui.',
  descricao:
    'Um saldo por assinatura. A escola decide quanto cada perfil usa.',
  pontos: [
    'Distribuição ajustável por perfil e turma',
    'Débito somente após resposta entregue',
    'Histórico de consumo por período',
  ],
}

/**
 * Depoimentos: placeholders até a instituição coletar relatos reais.
 * Não publique com texto fictício apresentado como real.
 */
export const depoimentos = [
  {
    texto: 'Espaço reservado para o relato de um professor da rede.',
    autor: 'Nome do professor',
    papel: 'Professor — a preencher',
  },
  {
    texto: 'Espaço reservado para o relato de um aluno usuário do tutor.',
    autor: 'Nome do aluno',
    papel: 'Aluno — a preencher',
  },
  {
    texto: 'Espaço reservado para o relato da direção da instituição.',
    autor: 'Nome do diretor',
    papel: 'Diretor — a preencher',
  },
]

export const ctaFinal = {
  titulo: 'Pronto para começar?',
  descricao: 'Configure a escola e distribua os primeiros créditos.',
  botao: 'Criar conta da instituição',
  apoio: 'Migração de dados com apoio da equipe.',
}

/** Contatos do rodapé. Paths de ícone em 24x24. */
export const contatos = [
  {
    rotulo: 'E-mail',
    href: '#',
    icone: 'M3 7l9 6 9-6M4 5h16a1 1 0 011 1v12a1 1 0 01-1 1H4a1 1 0 01-1-1V6a1 1 0 011-1z',
  },
  {
    rotulo: 'Para escolas',
    href: '#',
    icone: 'M3 8h18v11a1 1 0 01-1 1H4a1 1 0 01-1-1V8zM9 8V5a1 1 0 011-1h4a1 1 0 011 1v3',
  },
  {
    rotulo: 'Demonstração',
    href: '#',
    icone: 'M4 4h16a1 1 0 011 1v14a1 1 0 01-1 1H4a1 1 0 01-1-1V5a1 1 0 011-1zM10 9l5 3-5 3V9z',
  },
]

/** Indicador de disponibilidade exibido no rodapé. */
export const statusSistema = 'Plataforma operacional'

export const rodape = {
  colunas: [
    {
      titulo: 'Produto',
      links: [
        { rotulo: 'Como funciona', href: '#como-funciona' },
        { rotulo: 'Perfis', href: '#perfis' },
        { rotulo: 'Recursos', href: '#recursos' },
        { rotulo: 'Créditos', href: '#creditos' },
      ],
    },
    {
      titulo: 'Instituição',
      links: [
        { rotulo: 'Sobre', href: '#' },
        { rotulo: 'Contato', href: '#' },
        { rotulo: 'Suporte', href: '#' },
      ],
    },
    {
      titulo: 'Legal',
      links: [
        { rotulo: 'Privacidade', href: '#' },
        { rotulo: 'Termos de uso', href: '#' },
        { rotulo: 'Segurança', href: '#' },
      ],
    },
  ],
}
