/**
 * Destinos por perfil de usuário.
 *
 * ESTADO ATUAL: as telas de aluno, professor e diretor existem como
 * mockups estáticos no repositório de concepção `Estudo-com-IA`
 * (pasta `mockup/`), que ainda NÃO está publicado. Enquanto não
 * houver uma URL de verdade, `href` fica vazio e a interface mostra
 * o cartão como indisponível, em vez de levar a um link quebrado.
 *
 * COMO ATIVAR quando as telas estiverem no ar:
 *   1. publique os mockups (ex.: GitHub Pages no Estudo-com-IA);
 *   2. preencha `BASE_DESTINOS` com a URL publicada;
 *   3. nada mais precisa mudar - os cartões passam a navegar sozinhos.
 *
 * QUANDO O BACKEND EXISTIR, este arquivo deve ser substituído por
 * rotas internas com autenticação real. A escolha de perfil sem
 * senha é provisória: ela NÃO é um controle de acesso, apenas um
 * atalho de navegação enquanto não há login.
 */

/** Raiz onde os mockups estão publicados. Vazio = ainda indisponível. */
const BASE_DESTINOS = ''

export interface DestinoPerfil {
  id: 'aluno' | 'professor' | 'diretor'
  nome: string
  /** O que a pessoa faz nesta área, em uma linha. */
  resumo: string
  /** Vazio enquanto o destino não estiver publicado. */
  href: string
  corVar: string
  tintVar: string
}

export const destinos: DestinoPerfil[] = [
  {
    id: 'aluno',
    nome: 'Aluno',
    resumo: 'Tutor com memória, simulados e acompanhamento de notas.',
    href: BASE_DESTINOS ? `${BASE_DESTINOS}/aluno.html` : '',
    corVar: 'var(--color-aluno)',
    tintVar: 'var(--color-lavender-tint)',
  },
  {
    id: 'professor',
    nome: 'Professor',
    resumo: 'Geração de provas, correção assistida e banco de material.',
    href: BASE_DESTINOS ? `${BASE_DESTINOS}/professor.html` : '',
    corVar: 'var(--color-professor)',
    tintVar: 'var(--color-terracotta-tint)',
  },
  {
    id: 'diretor',
    nome: 'Diretor',
    resumo: 'Painéis por turma, gestão de usuários e distribuição de créditos.',
    href: BASE_DESTINOS ? `${BASE_DESTINOS}/diretor.html` : '',
    corVar: 'var(--color-diretor)',
    tintVar: 'var(--color-olive-tint)',
  },
]

/** Texto da tela de escolha. */
export const escolhaPerfil = {
  numero: '—',
  etiqueta: 'Entrar',
  titulo: 'Como você quer começar?',
  descricao:
    'Cada perfil abre uma área diferente da plataforma. Você poderá trocar depois.',
  indisponivel: 'Área em preparação',
}
