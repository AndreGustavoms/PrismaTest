/**
 * Conteudo da landing page do Prisma.
 * Texto separado da apresentacao: edite a copy aqui, sem tocar em JSX.
 */

export const marca = {
  nome: 'Prisma',
  descricao:
    'Plataforma de estudos com IA para instituicoes de ensino: um credito, tres perfis, memoria que acompanha o aluno.',
}

export const navegacao = [
  { rotulo: 'Como funciona', href: '#como-funciona' },
  { rotulo: 'Perfis', href: '#perfis' },
  { rotulo: 'Recursos', href: '#recursos' },
  { rotulo: 'Creditos', href: '#creditos' },
]

export const hero = {
  etiqueta: 'IA aplicada ao ensino',
  titulo: 'Uma entrada. Todo o espectro do ensino.',
  subtitulo:
    'O Prisma decompoe o trabalho pedagogico em ferramentas de IA para aluno, professor e diretor - com creditos controlados pela instituicao e memoria que acompanha cada aluno ao longo do ano.',
  ctaPrimario: 'Comecar agora',
  ctaSecundario: 'Ver como funciona',
  apoio: 'Sem cartao de credito. A instituicao define quanto cada perfil usa.',
}

/** Exemplos do demo do motor de refracao. */
export const exemplosRefracao = [
  {
    entrada: 'Fotossintese - 7o ano',
    saidas: ['Resumo guiado', 'Quiz de 10 questoes', 'Plano de aula'],
  },
  {
    entrada: 'Revolucao Francesa - Ensino Medio',
    saidas: ['Linha do tempo', 'Prova dissertativa', 'Material de apoio'],
  },
  {
    entrada: 'Fracoes - 5o ano',
    saidas: ['Lista progressiva', 'Exercicios resolvidos', 'Diagnostico'],
  },
  {
    entrada: 'Ciclo da agua - 4o ano',
    saidas: ['Mapa visual', 'Simulado curto', 'Roteiro de aula'],
  },
]

export const perfis = [
  {
    id: 'aluno',
    nome: 'Aluno',
    foco: 'Estudar com apoio continuo',
    corVar: 'var(--color-aluno)',
    itens: [
      'Tutor de IA que lembra o que voce ja estudou',
      'Textos de estudo no seu nivel',
      'Simulados com correcao comentada',
      'Notas e faltas em um so lugar',
    ],
  },
  {
    id: 'professor',
    nome: 'Professor',
    foco: 'Ensinar sem o trabalho repetitivo',
    corVar: 'var(--color-professor)',
    itens: [
      'Geracao de provas a partir do seu conteudo',
      'Correcao assistida, sempre com sua revisao',
      'Banco de material didatico reutilizavel',
      'Lancamento de notas integrado',
    ],
  },
  {
    id: 'diretor',
    nome: 'Diretor',
    foco: 'Administrar com visibilidade real',
    corVar: 'var(--color-diretor)',
    itens: [
      'Dashboards de desempenho por turma',
      'Gestao de usuarios, turmas e permissoes',
      'Distribuicao de creditos entre perfis',
      'Consumo de IA auditavel por periodo',
    ],
  },
]

export const recursos = [
  {
    titulo: 'Motor multi-modelo',
    descricao:
      'Cada tipo de tarefa - tutoria, geracao, correcao, resumo - vai para o modelo mais adequado em custo e qualidade.',
  },
  {
    titulo: 'Memoria persistente',
    descricao:
      'As sessoes viram resumos consolidados e datados. O tutor retoma o contexto do aluno sem reler tudo.',
  },
  {
    titulo: 'Creditos auditaveis',
    descricao:
      'Saldo derivado de um ledger unico. O debito so acontece depois de uma resposta bem-sucedida.',
  },
  {
    titulo: 'Revisao do professor',
    descricao:
      'Todo conteudo gerado por IA nasce rascunho. Prova e nota so valem apos aprovacao explicita de quem ensina.',
  },
  {
    titulo: 'Chave protegida',
    descricao:
      'Toda chamada de IA passa pelo backend. A credencial nunca chega ao navegador nem ao repositorio.',
  },
  {
    titulo: 'Painel por turma',
    descricao:
      'Acompanhe engajamento, evolucao e pontos de dificuldade sem montar planilha manual.',
  },
]

export const creditos = {
  etiqueta: 'Creditos',
  titulo: 'A instituicao assina. O diretor distribui.',
  descricao:
    'O credito e a unidade interna de consumo de IA. A instituicao recebe um saldo por assinatura e decide quanto cada professor e cada aluno pode usar.',
  pontos: [
    'Saldo unico por instituicao, derivado do ledger',
    'Distribuicao ajustavel por perfil e por turma',
    'Debito somente apos resposta entregue',
    'Historico completo de consumo por periodo',
  ],
}

/**
 * Depoimentos: placeholders ate a instituicao coletar relatos reais.
 * Nao publique com texto ficticio apresentado como real.
 */
export const depoimentos = [
  {
    texto: 'Espaco reservado para o relato de um professor da rede.',
    autor: 'Nome do professor',
    papel: 'Professor - a preencher',
  },
  {
    texto: 'Espaco reservado para o relato de um aluno usuario do tutor.',
    autor: 'Nome do aluno',
    papel: 'Aluno - a preencher',
  },
  {
    texto: 'Espaco reservado para o relato da direcao da instituicao.',
    autor: 'Nome do diretor',
    papel: 'Diretor - a preencher',
  },
]

export const ctaFinal = {
  titulo: 'Pronto para comecar?',
  descricao:
    'Configure a instituicao, cadastre as turmas e distribua os primeiros creditos.',
  botao: 'Criar conta da instituicao',
  apoio: 'Fale com a equipe se precisar migrar dados de outro sistema.',
}

export const rodape = {
  colunas: [
    {
      titulo: 'Produto',
      links: [
        { rotulo: 'Como funciona', href: '#como-funciona' },
        { rotulo: 'Perfis', href: '#perfis' },
        { rotulo: 'Recursos', href: '#recursos' },
        { rotulo: 'Creditos', href: '#creditos' },
      ],
    },
    {
      titulo: 'Instituicao',
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
        { rotulo: 'Seguranca', href: '#' },
      ],
    },
  ],
}
